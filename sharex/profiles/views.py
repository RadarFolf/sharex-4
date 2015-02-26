from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth

def logout_view(request):
	auth.logout(request)
	return redirect(reverse('landing_view'))
