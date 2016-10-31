from rest_framework import routers

from .views import user, user_profile, group

router = routers.DefaultRouter()

#register routes
router.register(r'users', user.UserViewSet)
router.register(r'groups', group.GroupViewSet)
router.register(r'user/profile', user_profile.UserProfileViewSet)