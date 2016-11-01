from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'', views.feed_view, name="rss_view"),
]