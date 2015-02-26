from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^', include('sharex.landing.urls')),
	url(r'^p/', include('sharex.profiles.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
