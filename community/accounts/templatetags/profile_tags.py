from django import template
from community.accounts.models import Profile, ProfileImage
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail
import os

register = template.Library()

@register.simple_tag
def avatar(user):
    profile = Profile.objects.get(user=user)
    try:
        avatar = ProfileImage.objects.get(profile=profile)
        image = avatar.image.url
    except ProfileImage.DoesNotExist:
        image = os.path.join(settings.MEDIA_URL, 'accounts/profiles/default.jpg')
    return format_html('''<img src="{}">''', image)
