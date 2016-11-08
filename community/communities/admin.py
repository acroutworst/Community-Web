from django.contrib import admin
from .models import Community, CommunityUserProfile

# Register your models here.
admin.site.register(Community)
admin.site.register(CommunityUserProfile)