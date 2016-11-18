from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name="events_index"),
    url(r'create_events/', views.create_events, name="create_events"),
    url(r'view_event/', views.view_event, name="view_event"),
]
