from django.contrib import admin

# Register your models here.
from .models import UserProfile, Community

admin.site.register(UserProfile)
admin.site.register(Community)