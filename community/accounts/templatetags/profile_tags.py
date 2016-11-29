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
        thumbnail = profile.image.thumbnail.url
        image = profile.image.image.url
        return format_html('<a href="{}"><img src="{}"></a>', image, thumbnail)
    except:
        image = os.path.join('/', settings.STATIC_URL, 'site/img/accounts/profiles/default.jpg')
        return format_html('<img src="{}">', image)
