from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_STATUS = (
        ('UNSEEN', 'unseen'),
        ('SEEN', 'seen'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    date = models.DateTimeField('notification date')
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='UNSEEN', blank=False, null=False)
    #Contenttype framework
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return "{0} {1}".format(self.description, self.date)

    class Meta:
        unique_together = ('user', 'id')
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'