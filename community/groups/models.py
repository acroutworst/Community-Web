from django.db import models


# Create your models here.
class Group(models.Model):
    CommunityID = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField (max_length = 30, blank = True, null = True)
    description = models.CharField(max_length=30, blank=True, null=True)
    groupDate = models.CharField(max_length=30, blank=True, null=True)
    LeaderName = models.CharField(max_length=30, blank=True, null=True)
    GroupID = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.title
