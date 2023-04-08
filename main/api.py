from .cors import CORSModelResource
from main.models import State, Party, Vote, Election
from django.db.models import Count, Sum
from tastypie.authorization import Authorization
from tastypie.resources import ALL_WITH_RELATIONS, ALL, fields


class StateResource(CORSModelResource):
	class Meta:
		queryset = State.objects.all()
		authorization = Authorization()


class ElectionResource(CORSModelResource):
	class Meta:
		queryset = Election.objects.all()
		authorization = Authorization()


class PartyResource(CORSModelResource):
	class Meta:
		queryset = Party.objects.all()
		authorization = Authorization()


class VoteResource(CORSModelResource):
	class Meta:
		queryset = Vote.objects.group_by('party', 'election').annotate(votes_count=Count('party'))
		include_resource_uri = False
		authorization = Authorization()
		filtering = {
			'id': ['exact'],
			'party': ALL_WITH_RELATIONS,
			'election': ALL_WITH_RELATIONS
		}
