from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_STATUS = (
        ('UNSEEN', 'unseen'),
        ('SEEN', 'seen'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    date = models.DateTimeField('notification date')
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='UNSEEN', blank=False, null=False)

    def __str__(self):
        return "{0} {1}".format(self.description, self.notif_date)

    class Meta:
        unique_together = ('user', 'notification_id')