from django import forms
from .models import Pirate

class ApplyPirateForm(forms.ModelForm):
	ship = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your startup'}))
	harbour = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter city'}))
	name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
	email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))

	class Meta:
		model = Pirate
		fields = ('name', 'email')

	def __init__(self, *args, **kwargs):
		super(ApplyPirateForm, self).__init__(*args, **kwargs)
		for f in self.fields:
			self.fields[f].widget.attrs['class'] = 'form-control'