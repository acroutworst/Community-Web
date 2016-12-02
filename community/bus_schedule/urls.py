from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.bus_schedule_view, name="bus_schedule_view"),
]