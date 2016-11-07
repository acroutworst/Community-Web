from django.db import models
from ..communities.models import Community
from django.contrib.auth.models import User


class Meetup(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', auto_now_add=True)
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=512, blank=True, null=True)
    #location
    max_attendees = models.IntegerField(blank=True, null=True)
    private = models.BooleanField(default=False)
    #tag

    class Meta:
        unique_together = ('community', 'creator', 'created_date')


class MeetupAttendee(models.Model):
    STATUS_CHOICES = (
        ('GOING', 'going'),
        ('PROBABLY', 'probably'),
        ('MIGHT', 'might'),
        ('NOT_GOING', 'not going'),
    )
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='GOING', blank=False, null=False)
    signup_time = models.DateTimeField('date joined', auto_created=True)
    updated = models.DateTimeField('last updated', auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meetup')