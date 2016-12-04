from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^search/', views.community_search_results, name="communities_search_results"),
    url(r'^$', views.communities_list, name="communities_list"),
    url(r'^(?P<slug>[\w-]+)/$', views.communities_view, name="communities_view"),
    url(r'^(?P<slug>[\w-]+)/join/$', views.communities_join, name="communities_join"),
    url(r'^(?P<slug>[\w-]+)/deactivate/$', views.communities_deactivate, name="communities_deactivate"),
    url(r'^(?P<slug>[\w-]+)/meetups/', include('community.meetups.community_urls')),

]