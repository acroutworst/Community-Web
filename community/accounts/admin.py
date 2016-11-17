from django.contrib import admin

# Register your models here.
from .models import Profile, ProfileImage

admin.site.register(Profile)
admin.site.register(ProfileImage)