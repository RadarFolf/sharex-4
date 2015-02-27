from django import forms
from .models import Profile, Startup
from sharex.landing.mails import WELCOME_EMAIL
from mixpanel import Mixpanel
from django.conf import settings
from django.core.mail import send_mail
import time

class InitialProfileCreationForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField()
	mixid = forms.CharField(required=False)

	def is_valid(self):
		valid = super(InitialProfileCreationForm, self).is_valid()
		if not valid:
			return valid
		if Profile.objects.filter(email=self.cleaned_data['email']).exists():
			self.errors['email'] = "Email already registered."
			return False
		return True

	def save(self):
		profile = Profile.objects.create_user(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
		mp = Mixpanel(settings.MIXPANEL_APPID)
		mixid = self.cleaned_data['mixid']
		mp.people_set(mixid, {
			'$email': profile.email,
			'$date_joined': profile.date_joined.isoformat(),
			})
		mp.alias(profile.id, mixid)
		send_mail(
			subject='Welcome to sharex.io',
			message=WELCOME_EMAIL,
			from_email='martin@sharex.io',
			recipient_list=[profile.email])
		return profile

class ApplyForm(forms.ModelForm):
	class Meta:
		model = Startup
		exclude = ('incubator',)

	def save(self, profile, *args, **kwargs):
		startup = super(ApplyForm, self).save(*args, **kwargs)
		profile.startup = startup
		profile.save()
		return startup
