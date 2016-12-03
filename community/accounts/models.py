from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.conf import settings
from io import BytesIO, StringIO, FileIO
from PIL import Image
import os

IMAGE_MAX_SIZE = 2000*2000
THUMBNAIL_RATIO = 1.2
THUMBNAIL_MAX_HEIGHT = 200
THUMBNAIL_MAX_WIDTH = THUMBNAIL_MAX_HEIGHT / THUMBNAIL_RATIO


def get_profile_image_path(instance, filename):
    return os.path.join('accounts', str(instance.profile.user.id), 'profile', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.CharField(max_length=60, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    image = models.OneToOneField('ProfileImage', related_name='profile_image', null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s profile"

    class Meta:
        unique_together = ('user', 'id')


class ProfileImage(models.Model):
    image = models.ImageField(null=False, upload_to=get_profile_image_path)
    thumbnail = models.ImageField(null=True, editable=False)
    profile = models.ForeignKey(Profile, related_name='profile_image', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(ProfileImage, self).save(*args, **kwargs)
        self.make_thumbnail()

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the image (simple resize with PIL).
        """
        fh = self.image.file
        try:
            image = Image.open(fh)
        except:
            return False
        w, h = image.size
        thumb_w, thumb_h = image.size
        if w > THUMBNAIL_MAX_WIDTH:
            thumb_w = THUMBNAIL_MAX_WIDTH
            thumb_h = int(thumb_w * THUMBNAIL_RATIO)
        if h > THUMBNAIL_MAX_HEIGHT:
            thumb_h = THUMBNAIL_MAX_HEIGHT
            thumb_w = int(thumb_h / THUMBNAIL_RATIO)
        thumb_size = thumb_w, thumb_h
        image.thumbnail(thumb_size, Image.ANTIALIAS)
        fh.close()

        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        return True

    def __str__(self):
        return "{}'s profile pic {}".format(self.profile.user.username, self.image.name)

    class Meta:
        unique_together = ('profile', 'id')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()