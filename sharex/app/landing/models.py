from django.db import models

class Harbour(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Ship(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Pirate(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField()
	harbour = models.ForeignKey(Harbour, related_name='pirates')
	ship = models.ForeignKey(Ship, related_name='pirates')

	def __unicode__(self):
		return self.name
