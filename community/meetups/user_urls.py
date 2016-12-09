from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.user_meetups_list, name="user_meetups_list"),
    url(r'^(?P<user_id>[\d]+)$', views.user_meetups_list, name="user_meetups_list"),
]