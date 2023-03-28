from django.contrib.gis.db import models


class Election(models.Model):
	name = models.CharField(max_length=75)
	active = models.BooleanField(default=True)


class State(models.Model):
	name = models.CharField(max_length=100)
	location = models.PointField(null=True, geography=True)


class Party(models.Model):
	abbr = models.CharField(max_length=5, unique=True)
	# we will use the `abbr` attribute to name the images
	name = models.CharField(max_length=100)


class Vote(models.Model):
	party = models.ForeignKey(Party, on_delete=models.CASCADE)
	total = models.IntegerField(default=0)
	state = models.ForeignKey(State, on_delete=models.CASCADE)
	election = models.ForeignKey('Election', on_delete=models.CASCADE)
