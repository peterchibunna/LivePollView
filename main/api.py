from .cors import CORSModelResource
from main.models import State, Party, Vote


class StateResource(CORSModelResource):
	class Meta:
		queryset = State.objects.all()


class PartyResource(CORSModelResource):
	class Meta:
		queryset = Party.objects.all()


class VoteResource(CORSModelResource):
	class Meta:
		queryset = Vote.objects.all()
