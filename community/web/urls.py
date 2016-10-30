from django.conf.urls import url, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='accounts/profile.html')),
    url(r'^groups/list', views.list_groups, name='list groups'),
]