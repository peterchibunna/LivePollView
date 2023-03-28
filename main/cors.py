"""
source: https://gist.github.com/miraculixx/6536381
Add CORS headers for tastypie APIs

Usage:
	class MyModelResource(CORSModelResource):
		...
	class MyResource(CORSResource):
		...

Authors:
	original source by http://codeispoetry.me/index.php/make-your-django-tastypie-api-cross-domain/
	extensions by @miraculixx
	* deal with ?format requests
	* always return CORS headers, even if always_return_data is False
	* handle exceptions properly (e.g. raise tastypie.BadRequests)
	* provide two distinct classes for ModelResource and Resource classes
"""
from functools import reduce

from django.http.response import HttpResponse
from tastypie import http
# from tastypie.contrib.gis.resources import ModelResource
from tastypie.exceptions import ImmediateHttpResponse
# from tastypie import resources
from tastypie.contrib.gis import resources
from tastypie.resources import Resource, csrf_exempt  # , ModelResource

from django.core.exceptions import (
	ObjectDoesNotExist, MultipleObjectsReturned, ValidationError, FieldDoesNotExist
)
from django.db.models.constants import LOOKUP_SEP
from tastypie.exceptions import (
	NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError,
	ImmediateHttpResponse, Unauthorized, UnsupportedFormat,
	UnsupportedSerializationFormat, UnsupportedDeserializationFormat,
)
from tastypie.utils import (
	# dict_strip_unicode_keys,
	is_valid_jsonp_callback_value, string_to_python,
	trailing_slash,
)
from tastypie.constants import ALL, ALL_WITH_RELATIONS


class ResourceMixin:
	pass


class ModelResource(ResourceMixin, resources.ModelResource):

	# def build_filters(self, filters=None, ignore_bad_filters=False):
	# 	""" Overrides BaseModelResource.build_filters to support query terms for related fields """
	#
	# 	if filters is None:
	# 		filters = {}
	#
	# 	qs_filters = {}
	#
	# 	for filter_expr, value in filters.items():
	# 		filter_bits = filter_expr.split(LOOKUP_SEP)
	# 		field_name = filter_bits.pop(0)
	#
	# 		if field_name not in self.fields:
	# 			# It's not a field we know about. Move along citizen.
	# 			continue
	#
	# 		try:
	# 			filter_type = self.resolve_filter_type(field_name, filter_bits, 'exact')
	# 			lookup_bits = self.check_filtering(field_name, filter_type, filter_bits)
	# 		except InvalidFilterError:
	# 			if ignore_bad_filters:
	# 				continue
	# 			else:
	# 				raise
	# 		value = self.filter_value_to_python(value, field_name, filters, filter_expr, filter_type)
	#
	# 		qs_filter = LOOKUP_SEP.join(lookup_bits)
	# 		qs_filters[qs_filter] = value
	#
	# 	return dict_strip_unicode_keys(qs_filters)

	def check_filtering(self, field_name, filter_type='exact', filter_bits=None):
		""" Overrides BaseModelResource.check_filtering to work with self.build_filters above """

		if filter_bits is None:
			filter_bits = []

		if field_name not in self._meta.filtering:
			raise InvalidFilterError("The '%s' field does not allow filtering." % field_name)

		# Check to see if it's an allowed lookup type.
		if filter_type != 'exact' and self._meta.filtering[field_name] not in (ALL, ALL_WITH_RELATIONS):
			# Must be an explicit whitelist.
			if filter_type not in self._meta.filtering[field_name]:
				raise InvalidFilterError("'%s' is not an allowed filter on the '%s' field." % (filter_type, field_name))

		if self.fields[field_name].attribute is None:
			raise InvalidFilterError("The '%s' field has no 'attribute' for searching with." % field_name)

		if len(filter_bits) == 0:
			# Only a field provided, match with provided filter type
			return [self.fields[field_name].attribute] + [filter_type]

		elif len(filter_bits) == 1 and filter_bits[0] in self.get_query_terms(field_name):
			# Match with valid filter type (i.e. contains, startswith, Etc.)
			return [self.fields[field_name].attribute] + filter_bits

		else:
			# Check to see if it's a relational lookup and if that's allowed.
			if not getattr(self.fields[field_name], 'is_related', False):
				raise InvalidFilterError("The '%s' field does not support relations." % field_name)

			if not self._meta.filtering[field_name] == ALL_WITH_RELATIONS:
				raise InvalidFilterError("Lookups are not allowed more than one level deep on the '%s' field." % field_name)

			# Recursively descend through the remaining lookups in the filter,
			# if any. We should ensure that all along the way, we're allowed
			# to filter on that field by the related resource.
			related_resource = self.fields[field_name].get_related_resource(None)

			next_field_name = filter_bits[0]
			next_filter_bits = filter_bits[1:]
			next_filter_type = related_resource.resolve_filter_type(next_field_name, next_filter_bits, filter_type)

			return [self.fields[field_name].attribute] + related_resource.check_filtering(next_field_name, next_filter_type, next_filter_bits)

	def get_query_terms(self, field_name):
		""" Helper to determine supported filter operations for a field """

		if field_name not in self.fields:
			raise InvalidFilterError("The '%s' field is not a valid field" % field_name)

		try:
			django_field_name = self.fields[field_name].attribute
			django_field = self._meta.object_class._meta.get_field(django_field_name)
			if hasattr(django_field, 'field'):
				django_field = django_field.field  # related field
		except FieldDoesNotExist:
			raise InvalidFilterError("The '%s' field is not a valid field name" % field_name)

		return django_field.get_lookups().keys()

	def resolve_filter_type(self, field_name, filter_bits, default_filter_type=None):
		""" Helper to derive filter type from next segment in filter bits """

		if not filter_bits:
			# No filter type to resolve, use default
			return default_filter_type
		elif filter_bits[0] not in self.get_query_terms(field_name):
			# Not valid, maybe related field, use default
			return default_filter_type
		else:
			# A valid filter type
			return filter_bits[0]


class BaseCorsResource(Resource):
	"""
	Class implementing CORS
	"""

	def error_response(self, *args, **kwargs):
		response = super(BaseCorsResource, self).error_response(*args, **kwargs)
		return self.add_cors_headers(response, expose_headers=True)

	def add_cors_headers(self, response, expose_headers=False):
		response['Access-Control-Allow-Origin'] = '*'
		response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
		if expose_headers:
			response['Access-Control-Expose-Headers'] = 'Location'
		return response

	def create_response(self, *args, **kwargs):
		"""
		Create the response for a resource. Note this will only
		be called on a GET, POST, PUT request if
		always_return_data is True
		"""
		response = super(BaseCorsResource, self).create_response(*args, **kwargs)
		return self.add_cors_headers(response)

	def post_list(self, request, **kwargs):
		"""
		In case of POST make sure we return the Access-Control-Allow Origin
		regardless of returning data
		"""
		# logger.debug("post list %s\n%s" % (request, kwargs));
		response = super(BaseCorsResource, self).post_list(request, **kwargs)
		return self.add_cors_headers(response, True)

	def post_detail(self, request, **kwargs):
		"""
		In case of POST make sure we return the Access-Control-Allow Origin
		regardless of returning data
		"""
		# logger.debug("post detail %s\n%s" (request, **kwargs));
		response = super(BaseCorsResource, self).post_list(request, **kwargs)
		return self.add_cors_headers(response, True)

	def put_list(self, request, **kwargs):
		"""
		In case of PUT make sure we return the Access-Control-Allow Origin
		regardless of returning data
		"""
		response = super(BaseCorsResource, self).put_list(request, **kwargs)
		return self.add_cors_headers(response, True)

	def put_detail(self, request, **kwargs):
		response = super(BaseCorsResource, self).put_detail(request, **kwargs)
		return self.add_cors_headers(response, True)

	def method_check(self, request, allowed=None):
		"""
		Check for an OPTIONS request. If so return the Allow- headers
		"""
		if allowed is None:
			allowed = []

		request_method = request.method.lower()
		allows = ','.join(map(lambda s: s.upper(), allowed))

		if request_method == 'options':
			response = HttpResponse(allows)
			response['Access-Control-Allow-Origin'] = '*'
			response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
			response['Access-Control-Allow-Methods'] = "GET, PUT, POST, PATCH, OPTIONS"
			response['Allow'] = allows
			raise ImmediateHttpResponse(response=response)

		if request_method not in allowed:
			response = http.HttpMethodNotAllowed(allows)
			response['Allow'] = allows
			raise ImmediateHttpResponse(response=response)

		return request_method

	def wrap_view(self, view):
		@csrf_exempt
		def wrapper(request, *args, **kwargs):
			request.format = kwargs.pop('format', None)
			wrapped_view = super(BaseCorsResource, self).wrap_view(view)
			return wrapped_view(request, *args, **kwargs)

		return wrapper


# Base Extended Abstract Model
class CORSModelResource(BaseCorsResource, ModelResource):
	def __init__(self, api_name=None):
		super().__init__(api_name=None)
		self.specified_fields = []

	def get_object_list(self, request):
		# import time
		# time.sleep(2)
		filters = super().build_filters()
		self.specified_fields = []
		objects = super().get_object_list(request)
		distinct = request.GET.get('distinct', False) == 'true'
		fields = request.GET.get("fields", False)
		if not fields:
			return objects
		try:
			self.specified_fields = fields.split(',')
		except:
			self.specified_fields.append(fields)

		# make `distinct` default for m2m filters
		has_m2m = False
		for field in filters:
			try:
				related = objects.model._meta.get_field_by_name(field)[0]
			except:
				related = False
			if related and related.get_internal_type() == 'ManyToManyField':
				has_m2m = True

		only_fields = []
		select_related = []

		for specified_field in self.specified_fields:

			try:
				fields = specified_field.split('__')
			except:
				continue

			# Only adds fields that exist for this model
			# excluding model methods
			for meta_field in objects.model._meta.fields:

				if meta_field.name == fields[0]:
					only_fields.append(specified_field)

			# Set `select_related` for related fields
			if len(fields) > 1:
				select_related.append('__'.join(fields[0:len(fields) - 1]))

		if len(only_fields):
			objects = objects.only(*only_fields)

		if len(self._meta.excludes):
			objects = objects.defer(*self._meta.excludes)

		if len(select_related):
			objects = objects.select_related(*select_related)

		if (has_m2m and not distinct) or distinct:
			objects = objects.distinct()

		return objects

	def full_dehydrate(self, bundle, for_list=False):

		"""
		This override disables `full=True` and other things we don't use
		"""

		# call the base class if qs param `fields` is not set
		if not len(self.specified_fields):
			return super().full_dehydrate(bundle, for_list)

		# Dehydrate each field supplied in the `fields` parameter
		for field_name, field_object in self.fields.items():

			# A touch leaky but it makes URI resolution work.
			if getattr(field_object, 'dehydrated_type', None) == 'related':
				field_object.api_name = self._meta.api_name
				field_object.resource_name = self._meta.resource_name

			# Check for an optional method to do further dehydration.
			method = getattr(self, "dehydrate_%s" % field_name, None)

			if method:
				bundle.data[field_name] = method(bundle)

		bundle = self.dehydrate(bundle)
		return bundle

	def dehydrate(self, bundle):

		# Dehydrate each field including related ones
		for row in self.specified_fields:

			f = row.split('__')

			bundle.data[row] = reduce(getattr, f, bundle.obj)

			# display actual values for `choices` fields
			method = getattr(bundle.obj, "get_%s_display" % f[0], False)
			if method:
				bundle.data[f[0]] = method()
		return bundle


class CORSResource(BaseCorsResource, Resource):
	pass
