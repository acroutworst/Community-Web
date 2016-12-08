from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.chatroom_view, name="chatroom_view"),
]