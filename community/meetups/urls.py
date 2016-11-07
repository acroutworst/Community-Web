from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.meetups_list(), name="meetups_list"),
    # url(r'^(?P<slug>[\w-]+)/$', views.communities_view, name="communities_view"),
    # url(r'^(?P<slug>[\w-]+)/join/$', views.communities_join, name="communities_join"),
    # url(r'^(?P<slug>[\w-]+)/deactivate/$', views.communities_deactivate, name="communities_deactivate"),
]