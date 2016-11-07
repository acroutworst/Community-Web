from django.contrib import admin
from .models import Meetup, Attendee
# Register your models here.
admin.site.register(Meetup)
admin.site.register(Attendee)