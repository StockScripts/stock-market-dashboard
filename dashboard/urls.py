from django.conf.urls import include, url

from .views import dashboard_view, search_view

urlpatterns = [
    url(r'^search=(?P<query>[\w-]+)/$', search_view),
    url(r'^$', dashboard_view),
]
