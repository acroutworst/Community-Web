from django.db import models
from ..communities.models import Community
from ..groups.models import Group
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Event(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now, auto_created=True)
    start_datetime = models.DateTimeField('date created', default=timezone.now)
    end_datetime = models.DateTimeField('date created', default=timezone.now)
    title = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=2048, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    private = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

class EventAttendee(models.Model):
    STATUS_CHOICES = (
        ('GOING', 'going'),
        ('PROBABLY', 'probably'),
        ('MIGHT', 'might'),
        ('NOT_GOING', 'not going'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_attendee')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='GOING', blank=False, null=False)
    signup_time = models.DateTimeField('date joined', auto_created=True)
    updated = models.DateTimeField('last updated', auto_now_add=True)

    def __str__(self):
        return "{0} is attending {1}".format(self.user, self.meetup)

    class Meta:
        unique_together = ('user', 'event')
