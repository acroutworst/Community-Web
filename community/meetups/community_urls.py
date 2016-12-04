from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.community_meetups_list, name="community_meetups_list"),
    url(r'^(?P<id>[\d]+)/$', views.meetups_view, name="meetups_view"),
    url(r'^(?P<id>[\d]+)/attend$', views.meetups_attend, name="meetups_attend"),
    url(r'^(?P<id>[\d]+)/changestatus$', views.meetup_change_status, name="meetups_change_status"),
    url(r'^create/$', views.meetups_create, name="meetups_create"),
]