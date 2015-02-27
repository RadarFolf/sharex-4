from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from .models import Startup, Profile

def logout_view(request):
	auth.logout(request)
	return redirect(reverse('landing_view'))

def signin_team(request, startup=None):
	if request.GET:
		if not startup:
			return redirect(reverse('landing_view'))
		try:
			s = Startup.objects.get(name=startup)
		except Startup.DoesNotExist:
			return redirect(reverse('landing_view'))
		try:
			p = Profile.objects.get(email=request.GET.get('email'))
		except Profile.DoesNotExist:
			return redirect(reverse('landing_view'))
		return render(request, 'landing/login_team.html', {'email': request.GET.get('email')})
	if request.POST:
		email = request.POST.get('email')
		password = request.POST.get('password')
		try:
			p = Profile.objects.get(email=email)
		except Profile.DoesNotExist:
			return render(request, 'landing/login_team.html', {'email': request.GET.get('email')})
		p.set_password(password)
		p.save()
		user = auth.authenticate(username=email, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect(reverse('success_view'))
	return redirect(reverse('landing_view')) 
