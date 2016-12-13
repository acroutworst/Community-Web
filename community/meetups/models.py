from django.db import models
from ..communities.models import Community
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime, timedelta
from . import tasks

class Meetup(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', auto_created=True)
    duration = models.IntegerField('duration (hours)', blank=False, null=False, default=2)
    name = models.CharField(max_length=128, blank=False, null=False)
    description = models.TextField(max_length=512, blank=True, null=True)
    max_attendees = models.IntegerField(blank=True, null=True)
    private = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    #tag

    def save(self, *args, **kwargs):
        create_task = False
        if self.pk is None:
            create_task = True
        super(Meetup, self).save(*args, **kwargs)
        if create_task:
            end_time = self.created_date + timedelta(hours=self.duration)
            try:
                tasks.set_inactive_after_time.apply_async((self.community.id, self.id), eta=end_time)
            except:
                pass

    def timeleft(self):
        endtime = self.endtime()
        now = timezone.now()
        timeleft = endtime - now
        seconds = timeleft.total_seconds()
        hoursleft = int(seconds // 3600)
        minutesleft = int(seconds // 60 % 60)
        secondsleft = int(seconds % 60)
        self.check_active(hoursleft, minutesleft, secondsleft)
        return hoursleft, minutesleft, secondsleft

    def endtime(self):
        time = self.created_date
        return time + timedelta(hours=self.duration)


    def check_active(self, hours, minutes, seconds):
        if self.active and (hours < 0 or minutes < 0 or seconds < 0):
            self.active = False
            self.save()
        return self.active

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
        attendee = Attendee.objects.create(meetup=instance, user=instance.creator, signup_time=datetime.now(), updated=datetime.now())
        attendee.save()


@receiver(post_save, sender=Meetup)
def save_meetup_creator_attendee(sender, instance, **kwargs):
    instance.attendee.get(meetup=instance, user=instance.creator).save()
