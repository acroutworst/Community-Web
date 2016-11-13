from django import template
from community.accounts.models import Profile, ProfileImage
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

register = template.Library()

@register.simple_tag
def avatar(user):
    profile = Profile.objects.get(user=user)
    avatar = ProfileImage.objects.get(profile=profile)
    return format_html('''<img src="{}">''', avatar.image.url)
