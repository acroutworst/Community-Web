from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from graphene_django.views import GraphQLView
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
    url(r'^chatroom/', include ('community.chatroom.urls')),
    url(r'^notifications/', include('community.notifications.urls')),
    url(r'^meetups/', include('community.meetups.user_urls')),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
