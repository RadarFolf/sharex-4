from django import forms
from .models import Pirate, Ship, Harbour
from django.core.mail import send_mail

class ApplyPirateForm(forms.ModelForm):
	ship = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter startup'}))
	harbour = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter city'}))
	name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter name'}))
	email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter email'}))
	motivation = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'placeholder': 'Give us a speech, eh? Keep it short!'}))
	
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
		send_mail("Ahoy from ShareX!",
"""Ahoy, pirate! Thanks for applying for the fleet. ShareX mission is to gather all you entrepreneurs as pirates - to connect with each other and unite our resources.
ShareX is the place to learn about the goals, processes and struggles of other entrepreneurs faring the unchartered waters.
Soon you can share, explore and observe, but first we want to get to know all of you pirates a little better to make a page for your needs.

Any feedback or questions will be greatly appreciated. Feel free to add me on skype or send me an email.

So long, you'll hear from us soon! In the meantime fair winds and following seas,
Marius Norheim, Co-founder of ShareX
Skype: marnor28
mail: marius.norheim@gmail.com""",
"teamsharex@gmail.com",
			[pirate.email],
			fail_silently=False)
		return pirate