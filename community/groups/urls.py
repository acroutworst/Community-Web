from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.groups_list, name="groups_list"),
    url(r'^(?P<id>[\d]+)/$', views.groups_view, name = "groups_view"),
]