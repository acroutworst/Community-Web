from django.db import models
from django.contrib.auth.models import User

from community.friendlist.models import FriendList

FILTER_CHOICES = (
    ('GENERAL','General'),
    ('CLASSMATES','Classmates'),
    ('COWORKERS','Coworkers'),
)

# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey(User)
    friend_list = models.ForeignKey(FriendList)
    added_date = models.DateTimeField(auto_created=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    filter = models.CharField(max_length=10, choices=FILTER_CHOICES, default='GENERAL', blank=False, null=False)

    class Meta:
        unique_together = ('user','friendlist')