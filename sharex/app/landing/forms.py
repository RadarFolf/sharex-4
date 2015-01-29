from django import forms
from .models import Pirate, Ship, Harbour

class ApplyPirateForm(forms.ModelForm):
	ship = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your startup'}))
	harbour = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter city'}))

	class Meta:
		model = Pirate
		fields = ('name', 'email', 'motivation')

	def save(*args, **kwargs):
		kwargs['commit'] = False
		pirate = super(ApplyPirateForm, self).save(*args, **kwargs)
		ship, _ = Ship.objects.get_or_create(name=self.cleaned_data['ship'].strip().lower())
		harbour, _ = Harbour.objects.get_or_create(name=self.cleaned_data['harbour'].strip().lower())
		pirate.ship = ship
		pirate.harbour = harbour
		pirate.save()
		return pirate