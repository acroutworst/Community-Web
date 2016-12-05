from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.notifications_view, name="notifications_view"),
]