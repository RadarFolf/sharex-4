from django.db import models
from django.utils import timezone as dtimezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import pytz
import re

def valid_email(email):
	EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
	if EMAIL_REGEX.match(email):
		return True
	return False

class ProfileManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email or not valid_email(email):
			raise ValueError('Profile needs an email address')
		user = self.model(
			email=self.normalize_email(email),
			**extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
			email=email,
			password=password,
			is_superuser=True,
			is_staff=True)
		user.save(using=self._db)
		return user

class Profile(AbstractBaseUser, PermissionsMixin):
	timezone = models.CharField(max_length=100, choices = [(x, x) for x in pytz.common_timezones], default='Europe/London')
	name = models.CharField(max_length=50, blank=True, null=True)
	display_name = models.CharField(max_length=20, blank=True, null=True)
	email = models.EmailField(max_length=255, unique=True)
	is_staff = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=dtimezone.now)
	startup = models.ForeignKey('profiles.Startup', related_name='profiles', blank=True, null=True)
	token = models.CharField(max_length=150, blank=True, null=True)
	USERNAME_FIELD = 'email'

	objects = ProfileManager()

	def get_full_name(self):
		return self.name

	def get_short_name(self):
		return self.display_name

	def __unicode__(self):
		return self.email

class Incubator(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name


class Startup(models.Model):
	name = models.CharField(max_length=50)
	incubator = models.ForeignKey(Incubator, related_name='startups', blank=True, null=True)
	website = models.URLField(max_length=80, blank=True, null=True)
	pitch = models.TextField()
	revenuemodels = models.TextField(blank=True, null=True)
	last_milestone = models.TextField(blank=True, null=True)
	next_milestone = models.TextField(blank=True, null=True)
	additional = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.name
