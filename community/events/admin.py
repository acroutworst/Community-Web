from django.contrib import admin
from .models import Event, EventAttendee, EventImage
admin.site.register(Event)
admin.site.register(EventAttendee)
admin.site.register(EventImage)
# Register your models here.
