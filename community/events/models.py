from django.db import models
from ..communities.models import Community
from ..groups.models import Group
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from easy_thumbnails.fields import ThumbnailerImageField

def get_event_image_path(instance, filename):
    if instance.event.group:
        return os.path.join('community', str(instance.event.community.id), 'group', str(instance.event.group.id), 'events', filename)
    return os.path.join('community', str(instance.event.community.id), 'events', filename)

class Event(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now, auto_created=True)
    start_datetime = models.DateTimeField('date created', default=timezone.now)
    end_datetime = models.DateTimeField('date created', default=timezone.now)
    title = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=2048, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    private = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    image = models.ForeignKey('EventImage', on_delete=models.SET_NULL, blank=True, null=True, default=None, related_name='current_event_image')

    def attendee_count(self):
        return len(EventAttendee.objects.filter(event=self, status='GOING'))

    def __str__(self):
        return self.title

class EventImage(models.Model):
    image = ThumbnailerImageField(null=False, upload_to=get_event_image_path)
    event = models.ForeignKey(Event, related_name='event_image', on_delete=models.CASCADE)

    def __str__(self):
        return "{} pic: {}".format(self.event.title, self.image.name)

    class Meta:
        unique_together = ('event', 'id')

class EventAttendee(models.Model):
    STATUS_CHOICES = (
        ('GOING', 'going'),
        ('INTERESTED', 'interested'),
        ('NOT_GOING', 'not going'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_attendee')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='GOING', blank=False, null=False)
    signup_time = models.DateTimeField('date joined', auto_created=True)
    updated = models.DateTimeField('last updated', auto_now_add=True)

    def __str__(self):
        return "{0} is attending {1}".format(self.user, self.event)

    class Meta:
        unique_together = ('user', 'event')
