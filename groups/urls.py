from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^list', views.list_groups, name='list groups'),
]