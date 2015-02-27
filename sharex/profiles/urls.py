from django.conf.urls import patterns, url
from .views import logout_view, signin_team

urlpatterns = patterns('',
	url(r'logout/$', logout_view, name='logout_view'),
	url(r'^signup/(?P<startup>\w+)/$', signin_team, name='signin_team'),
	url(r'^signup/$', signin_team, name='signin_team'),
)