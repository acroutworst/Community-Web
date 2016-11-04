from django.db import models

# Create your models here.
class Community(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=512, blank=True, null=True)