from django.conf.urls import include, url

from .views import (
	dashboard_view,
	profile_view,
	refresh_view,
	search_view,
)

urlpatterns = [
	url(r'^profile$', profile_view),
	url(r'^refresh=(?P<series>[0-9]{1})$', refresh_view),
	url(r'^search=(?P<query>[\w-]+)/$', search_view),
	url(r'^$', dashboard_view),
]
