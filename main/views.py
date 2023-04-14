from django.contrib.gis.geos import Point
from django.http.response import HttpResponse
from django.shortcuts import render

from main.models import State, Party, Vote, Election


def acme_challenge(request, codes):
	"""
	view that certbot uses to verify the domain during SSL certificate generation
	"""
	full_code = ''
	return HttpResponse(full_code)


def index(request):
	"""
	The main app's page showing the map.
	From here the api calls are made to load the markers for the states
	"""
	return render(request, 'map.html', {})


def votes_view_modal(request):
	"""
	fetch the votes for each political party according to the selected state and election
	"""
	state = State.objects.get(pk=request.GET.get('state_id'))
	election = Election.objects.get(pk=request.GET.get('election_id'))
	votes = []
	for party in Party.objects.all():
		data = Vote.objects.get_or_create(election=election, party=party, state=state)[0]
		votes.append(
			dict(party=party, total=data.total)
		)

	return render(request, 'votes.html', {'votes': sorted(votes, key=lambda i: i['total'], reverse=True), 'state': state, 'election': election})
