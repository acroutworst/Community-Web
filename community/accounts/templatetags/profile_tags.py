from django import template
from ..models import Profile, ProfileImage
from django.conf import settings
from django.utils.html import format_html
import os

register = template.Library()

@register.simple_tag
def avatar(user):
    profile = Profile.objects.get(user=user)
    try:
        image = profile.image.image.url
    except:
        image = os.path.join(settings.MEDIA_URL, 'accounts/profiles/default.jpg')

    return format_html('<img src="{}">', image)
