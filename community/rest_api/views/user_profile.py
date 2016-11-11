from rest_framework import viewsets

from community.accounts.models import Profile
from ..serializers.user_profile import UserProfileSerializer


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer