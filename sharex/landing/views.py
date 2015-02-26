from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from sharex.profiles.models import Profile
from sharex.profiles.forms import InitialProfileCreationForm, ApplyForm

from django.conf import settings
from mixpanel import Mixpanel
mp = Mixpanel(settings.MIXPANEL_APPID)

def landing_view(request):
	if request.POST:
		form = InitialProfileCreationForm(request.POST)
		if form.is_valid():
			profile = form.save()
			user = auth.authenticate(username=profile.email, password=form.cleaned_data['password'])
			if user is not None:
				auth.login(request, user)
				return redirect(reverse('apply_view'))
		else:
			print form.errors
	return render(request, 'landing/landing.html')

@login_required
def apply_view(request):
	if request.POST:
		form = ApplyForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			return redirect(reverse('pay_view'))
		else:
			print form.errors
	return render(request, 'landing/apply.html')

@login_required
def pay_view(request):
	if request.user.startup is None:
		return redirect(reverse('apply_view'))
	if request.POST:
		if 'token' in request.POST:
			token = request.POST.get('token')
			if token:
				mp.people_set(request.user.id, {'$plan': 'Pro'})
				request.user.token = token
				request.user.save()
		return redirect(reverse('success_view'))
	return render(request, 'landing/pay.html')

@login_required
def success_view(request):
	if request.user.startup is None:
		return redirect(reverse('apply_view'))
	if request.user.token is None:
		plan = 'Free'
	else:
		plan = 'Pro'
	mp.people_set(request.user.id, {'$plan': plan})
	return render(request, 'landing/success.html', {'count_profiles': Profile.objects.count()+41})

def login_view(request):
	if request.POST:
		email = request.POST.get('email', False)
		password = request.POST.get('password', False)
		if email and password:
			user = auth.authenticate(username=email, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect(reverse('success_view'))
	return render(request, 'landing/login.html')