from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=60, blank=True, null=True)
    department = models.CharField(max_length=60, blank=True, null=True)
    interests = models.CharField(max_length=60, blank=True, null=True)
    transportation = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.user.username + "'s profile"