from django.db import models

class Harbour(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Ship(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Pirate(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	harbour = models.ForeignKey(Harbour, related_name='pirates')
	ship = models.ForeignKey(Ship, related_name='pirates')
	motivation = models.CharField(max_length=250, blank=True, null=True)

	def __unicode__(self):
		return self.name
