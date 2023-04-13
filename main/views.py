from django.contrib.gis.geos import Point
from django.http.response import HttpResponse
from django.shortcuts import render

from main.models import State, Party, Vote, Election


def acme_challenge(request, codes):
	full_code = ''
	return HttpResponse(full_code)

def index(request):
	return render(request, 'map.html', {})


def test_view(request):
	state = State.objects.get(pk=request.GET.get('state_id'))
	election = Election.objects.get(pk=request.GET.get('election_id'))
	votes = []
	for party in Party.objects.all():
		data = Vote.objects.get_or_create(election=election, party=party, state=state)[0]
		votes.append(
			dict(party=party, total=data.total)
		)

	return render(request, 'votes.html', {'votes': sorted(votes, key=lambda i: i['total'], reverse=True), 'state': state, 'election': election})


def import_state_gps_locations():
	locations = [
		('ABIA', (5.599636065783628, 7.581137487836031)), ('ADAMAWA', (9.195365508217208, 12.490403509491784)), ('AKWA IBOM', (5.022510701624171, 7.933981896372586)), ('ANAMBRA', (6.246426847750172, 6.919580878114402)),
		('BAUCHI', (10.35014812647617, 9.851144791013724)), ('BAYELSA', (4.932306930607126, 6.272367018311655)), ('BENUE', (7.385453194845098, 8.468463733915428)), ('BORNO', (11.769428425405096, 13.2182234090929)),
		('CROSS RIVER', (4.994523024758237, 8.345871613638167)), ('DELTA', (6.166096988416328, 6.66393985127732)), ('EBONYI', (6.324112018307346, 8.113882655986487)), ('EDO', (6.324804402566642, 5.630579685253707)),
		('EKITI', (7.608936234300316, 5.230225996382671)), ('ENUGU', (6.440531253917399, 7.492183010155912)), ('FEDERAL CAPITAL TERRITORY', (9.058170880515718, 7.371404434185479)), ('GOMBE', (10.295475670636748, 11.172033754160367)),
		('IMO', (5.487184616072355, 7.051206063043509)), ('JIGAWA', (12.176884759520107, 9.483883351570512)), ('KADUNA', (10.293585627704246, 7.901919558167947)), ('KANO', (11.740607643189321, 8.66686829989112)),
		('KATSINA', (12.625149950392995, 7.670918769483109)), ('KEBBI', (12.066517713705295, 4.237552330761474)), ('KOGI', (7.793911551277844, 6.763666788596851)), ('KWARA', (8.50693771269448, 4.530928588470431)),
		('LAGOS', (6.453505933420288, 3.410522684962473)), ('NASARAWA', (9.648555072136219, 11.830719956320678)), ('NIGER', (9.717608564604205, 5.9722752813263185)), ('OGUN', (7.16035544342283, 3.34599868454427)),
		('ONDO', (7.24160637264157, 5.198102976986746)), ('OSUN', (7.76765675947334, 4.560180390539728)), ('OYO', (7.380427328567265, 3.889742141326934)), ('PLATEAU', (9.930483238894652, 8.90390646061465)),
		('RIVERS', (4.771454007252345, 7.025960421244349)), ('SOKOTO', (13.051421335895725, 5.23679165568285)), ('TARABA', (8.88742425734742, 11.377408205709514)), ('YOBE', (12.41246299131761, 11.423779075544417)),
		('ZAMFARA', (12.104700668397697, 6.219725042579427))
	]
	for i in locations:
		a = State.objects.get_or_create(name=i[0], location=Point(i[1][0], i[1][1]))
		print(a)
