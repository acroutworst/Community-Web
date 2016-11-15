from django.db import models
from ..communities.models import Community
from django.contrib.auth.models import User

class Group(models.Model):
    community = models.ForeignKey (Community, on_delete = models.CASCADE)
    description = models.CharField (max_length = 300, blank = True, null = True)
    create_date = models.DateTimeField ('date created', auto_created = True)
    create_by = models.CharField (max_length = 30, blank = True, null = True)
    current_leader = models.CharField (max_length = 30, blank = True, null = True)
    title = models.CharField (max_length = 50, blank = False, null = False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('community', 'id')


class Group_Members(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    community = models.ForeignKey(Community, on_delete = models.CASCADE)
    position = models.CharField(max_length = 30, blank = True, null = True)
    join_date = models.DateTimeField('date joined', auto_created = True)
    last_activity = models.CharField(max_length = 300, blank = True, null = True)

    def __str__(self):
        return self.user

    class Meta:
        unique_together = ('user', 'id', 'community', 'group')






# Create your models here.
