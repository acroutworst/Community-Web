from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .events import views

urlpatterns = [
    url(r'^events/$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('community.rest_api.urls')),
    url(r'^accounts/', include('community.accounts.urls')),
    url(r'^groups/', include('community.groups.urls')),
    url(r'^rss/', include('community.rss_feed.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
