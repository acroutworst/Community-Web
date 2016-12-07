from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.groups_list, name="groups_list"),
    url(r'^(?P<id>[\d]+)/$', views.groups_view, name = "groups_view"),
    url(r'^(?P<id>[\d]+)/join/$', views.group_join, name = "groups_join"),
    url(r'^(?P<id>[\d]+)/member/$', views.group_member_view, name="groups_member"),
    url(r'^(?P<id>[\d]+)/deactivate/$', views.group_deactivate, name ="groups_deactivate"),
    url(r'^create', views.group_create, name="groups_create"),
]