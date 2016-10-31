from django.conf.urls import url, include
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = [
    url('', include('allauth.urls')),
    url(r'^profile/$', TemplateView.as_view(template_name='accounts/profile.html')),
]