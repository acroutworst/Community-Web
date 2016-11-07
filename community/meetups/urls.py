from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.meetups_list, name="meetups_list"),
    url(r'^(?P<id>[\d]+)/$', views.meetups_view, name="meetups_view"),
    url(r'^(?P<id>[\d]+)/attend$', views.meetups_attend, name="meetups_attend"),
    # url(r'^(?P<slug>[\w-]+)/$', views.communities_view, name="communities_view"),
    url(r'^create/$', views.meetups_create, name="meetups_create"),
    # url(r'^(?P<slug>[\w-]+)/deactivate/$', views.communities_deactivate, name="communities_deactivate"),
]