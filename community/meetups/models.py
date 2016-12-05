from django.db import models

from community.notifications.models import Notification
from django.contrib.contenttypes.fields import GenericRelation
from ..communities.models import Community
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class Meetup(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', auto_created=True)
    duration = models.IntegerField('duration (hours)', blank=False, null=False, default=2)
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=512, blank=True, null=True)
    #location
    max_attendees = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    private = models.BooleanField(default=False)
    #tag
    notification = GenericRelation(Notification)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('community', 'id')


class Attendee(models.Model):
    STATUS_CHOICES = (
        ('GOING', 'going'),
        ('PROBABLY', 'probably'),
        ('MIGHT', 'might'),
        ('NOT_GOING', 'not going'),
    )
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE, related_name='attendee')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='GOING', blank=False, null=False)
    signup_time = models.DateTimeField('date joined', auto_created=True)
    updated = models.DateTimeField('last updated', auto_now_add=True)

    def __str__(self):
        return "{0} is attending {1}".format(self.user, self.meetup)

    class Meta:
        unique_together = ('user', 'meetup')


@receiver(post_save, sender=Meetup)
def create_meetup_creator_attendee(sender, instance, created, **kwargs):
    if created:
        attendee = Attendee.objects.create(meetup=instance, user=instance.creator, signup_time=datetime.datetime.now(), updated=datetime.datetime.now())
        attendee.save()


@receiver(post_save, sender=Meetup)
def save_meetup_creator_attendee(sender, instance, **kwargs):
    instance.attendee.get(meetup=instance, user=instance.creator).save()
