from django.db import models

class Event(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    private = models.BooleanField()
    image = models.ImageField()
    description = models.TextField()
