from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('', include('allauth.urls')),
    url(r'^profile/$', views.profile_view, name="accounts_profile"),
    url(r'^profile/edit', views.profile_edit),
]