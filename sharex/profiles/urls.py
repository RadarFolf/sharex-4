from django.conf.urls import patterns, url
from .views import logout_view

urlpatterns = patterns('',
	url(r'logout/$', logout_view, name='logout_view'),
)