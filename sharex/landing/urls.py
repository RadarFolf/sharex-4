from django.conf.urls import patterns, url
from .views import landing_view, apply_view, pay_view, success_view, login_view

urlpatterns = patterns('',
	url(r'^$', landing_view, name='landing_view'),
	url(r'^apply/$', apply_view, name='apply_view'),
	url(r'^pay/$', pay_view, name='pay_view'),
	url(r'^success/$', success_view, name='success_view'),
	url(r'^login/$', login_view, name='login_view'),
)