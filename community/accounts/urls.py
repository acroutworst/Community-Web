from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('', include('allauth.urls')),
    url(r'^profile/((?P<userid>[0-9]+)/{0,1}){0,1}$', views.profile_view, name="accounts_view_profile"),
    url(r'^profile/edit', views.profile_edit, name="accounts_profile_edit"),
    url(r'^profile/image/upload', views.profile_image_upload, name="accounts_image_upload"),
]