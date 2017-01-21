from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
import oauth2_provider.views as oauth2_views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import ProtectedGraphQLEndpoint
from . import views

oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]

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
    url(r'^api', ProtectedGraphQLEndpoint.as_view()),
    url(r'^o/', include(oauth2_endpoint_views, namespace="oauth2_provider")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))))
