from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
