from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name="events_index"),
    url(r'create_events/', views.create_events, name="create_events"),
    #url(r'view_event/', views.view_event, name="view_event"),
    url(r'^events/(?P<event_id>[0-9]+)/$', views.view_event, name="view_event"),
]
# url(r'^clubs/(?P<club_id>[\w]+)/events/create$', EventCreateView.as_view(), name='event_create'),
#     url(r'^clubs/(?P<club_id>[\w]+)/events/(?P<event_id>[0-9]+)/$', EventView.as_view()),

#url(r'^events/(?P<event_id>[0-9]+)/$', view_event.as_view

# urlpatterns = [
#     url(r'^$', views.index, name="events_index"),
#     url(r'create_events/', views.create_events, name="create_events"),
#     url(r'view_event/', views.view_event, name="view_event"),
# ]