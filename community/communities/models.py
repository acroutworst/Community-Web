from django.db import models
from django.contrib.auth.models import User
from community.notifications.models import Notification
from django.contrib.contenttypes.fields import GenericRelation


class Community(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    acronym = models.CharField(max_length=5, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    #location = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_created=True)
    slug = models.SlugField(max_length=40, db_index=True, unique=True)
    # notification = GenericRelation(Notification)

    def __str__(self):
        return self.title + " ({0})".format(self.acronym)

    class Meta:
        verbose_name_plural = 'Communities'


class CommunityUserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    department = models.CharField(max_length=128, blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.community.acronym:
            return self.user.username + "\'s {0} Profile".format(self.community.acronym)
        else:
            return self.user.username + "\'s {0} Profile".format(self.community.title)

    class Meta:
        unique_together = ('user', 'community')
