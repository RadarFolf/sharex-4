from django import forms
from .models import Pirate, Ship, Harbour

class ApplyPirateForm(forms.ModelForm):
	ship = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter startup'}))
	harbour = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter city'}))
	name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter name'}))
	email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
	motivation = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'placeholder': 'Give us a speech, eh?'}))
	
	def __init__(self, *args, **kwargs):
		super(ApplyPirateForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'

	class Meta:
		model = Pirate
		fields = ('name', 'email', 'motivation')

	def save(self, *args, **kwargs):
		kwargs['commit'] = False
		pirate = super(ApplyPirateForm, self).save(*args, **kwargs)
		ship, _ = Ship.objects.get_or_create(name=self.cleaned_data['ship'].strip().lower())
		harbour, _ = Harbour.objects.get_or_create(name=self.cleaned_data['harbour'].strip().lower())
		pirate.ship = ship
		pirate.harbour = harbour
		pirate.save()
		return pirate