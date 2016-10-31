from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url('', include('allauth.urls')),
    url(r'^profile/$', views.profile_view, name="accounts_profile"),
    url(r'^profile/edit', views.profile_edit),
]