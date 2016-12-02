from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^events/', include('community.events.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('community.rest_api.urls')),
    url(r'^accounts/', include('community.accounts.urls')),
    url(r'^communities/', include('community.communities.urls')),
    url(r'^groups/', include('community.groups.urls')),
    url(r'^rss/', include('community.rss_feed.urls')),
    url(r'^bus_schedule/', include ('community.bus_schedule.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
