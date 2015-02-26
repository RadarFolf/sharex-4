from django import forms
from .models import Profile, Startup
from mixpanel import Mixpanel
from django.conf import settings

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
			})
		mp.alias(profile.id, mixid)
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
