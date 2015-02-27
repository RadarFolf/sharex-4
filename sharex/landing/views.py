from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from sharex.profiles.models import Profile
from sharex.profiles.forms import InitialProfileCreationForm, ApplyForm
from django.core.mail import send_mail

from .mails import get_invite_email

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
			for _, error in form.errors.items():
				messages.info(request, error)
	return render(request, 'landing/landing.html')

@login_required
def apply_view(request):
	if request.POST:
		form = ApplyForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			mp.people_set(request.user.id, {'$startup': request.user.startup.name})
			return redirect(reverse('pay_view'))
		else:
			for k, v in form.errors.as_data().items():
				messages.info(request, "%s %s" % (v[0].messages[0], k.title()))
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
	if request.POST:
		for email in request.POST.get('emails').split(','):
			try:
				if not Profile.objects.filter(email=email).exists():
					Profile.objects.create_user(email=email, password='123', startup_id=request.user.startup.id)
				send_mail(
					subject='You got invited to sharex.io',
					message=get_invite_email(request.user.email, email, request.user.startup.name),
					from_email='martin@sharex.io',
					recipient_list=[email])
			except Exception, e:
				messages.info(request, e.message)
	mp.people_set(request.user.id, {'$plan': plan})
	return render(request, 'landing/success.html', {'count_profiles': Profile.objects.count()+41, 'emails': request.user.startup.profiles.all().values_list('email', flat=True)})

def login_view(request):
	if request.POST:
		email = request.POST.get('email', False)
		password = request.POST.get('password', False)
		if email and password:
			user = auth.authenticate(username=email, password=password)
			if user is not None:
				auth.login(request, user)
				return redirect(reverse('success_view'))
			else:
				messages.info(request, "Wrong email and password")
		else:
			messages.info(request, "Enter email and password")
	return render(request, 'landing/login.html')