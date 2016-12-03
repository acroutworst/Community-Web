from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class FriendList(models.Model):
    friend_list_id = models.AutoField()
    user = models.ForeignKey(User)