from rest_framework import viewsets

from accounts.models import UserProfile
from ..serializers.user_profile import UserProfileSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer