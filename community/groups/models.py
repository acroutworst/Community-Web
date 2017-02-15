from django.db import models
from ..communities.models import Community
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

def get_group_image_path(instance, filename):
    return os.path.join('community', str(instance.group.community.id), 'group', str(instance.group.id), filename)

class Group(models.Model):
    community = models.ForeignKey(Community, on_delete = models.CASCADE)
    description = models.CharField (max_length = 300, blank = True, null = True)
    create_date = models.DateTimeField ('date created', auto_created = True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField (max_length = 50, blank = False, null = False)
    current_leader = models.ForeignKey(User, related_name= 'leader', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    image = models.ForeignKey('GroupImage', on_delete=models.SET_NULL, null=True, default=None, related_name='current_group_image')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('community', 'id')


class GroupImage(models.Model):
    image = ThumbnailerImageField(null=False, upload_to=get_group_image_path)
    group = models.ForeignKey(Group, related_name='group_image', on_delete=models.CASCADE)

    def __str__(self):
        return "{} pic: {}".format(self.group.title, self.image.name)

    class Meta:
        unique_together = ('group', 'id')


class GroupMembers(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    position = models.CharField(max_length = 30, blank = True, null = True)
    join_date = models.DateTimeField('date joined', auto_created = True)
    last_activity = models.DateTimeField('last activity', auto_created=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user

    class Meta:
        unique_together = ('user', 'group')






# Create your models here.
