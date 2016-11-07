from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)


class CommunityUserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    department = models.CharField(max_length=128, blank=True, null=True)
    position = models.CharField(max_length=128, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'community')
