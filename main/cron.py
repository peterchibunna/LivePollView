from main.models import Vote, Party, Election, State
import random


def do_vote():
	"""
	randomly increase the votes of each political party
	in each state, for each election type
	:return:
	"""
	for election in Election.objects.all():
		for state in State.objects.all():
			for party in Party.objects.all():
				v = Vote.objects.get_or_create(party=party, state=state, election=election)[0]
				v.total += random.randint(1, 100)
				v.save()
	pass
