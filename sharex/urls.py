from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$', 'sharex.app.landing.views.index', name='landing'),
    url(r'^admin/', include(admin.site.urls)),
)
