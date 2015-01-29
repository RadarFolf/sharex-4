from django.shortcuts import render
from .forms import ApplyPirateForm

def index(request):
	if request.POST:
		print 'Got form'
		form = ApplyPirateForm(request.POST)
		return render(request, 'landing/index.html', {'form': form})
	return render(request, 'landing/index.html', {'form': ApplyPirateForm()})