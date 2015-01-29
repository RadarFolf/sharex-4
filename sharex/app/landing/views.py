from django.shortcuts import render
from .forms import ApplyPirateForm
from django.contrib import messages

def index(request):
	modal_popup = 0
	if request.POST:
		form = ApplyPirateForm(request.POST)
		if form.is_valid():
			pirate = form.save()
			messages.success(request, "You have successfully applied to join the fleet! We will get back to you soon. AHOY!")
		else:
			messages.info(request, "Something went wrong with your application, eh. Try to fix it!")
			modal_popup = 1
	else:
		form = ApplyPirateForm()
	return render(request, 'landing/index.html', {'form': form, 'modal_popup': modal_popup})