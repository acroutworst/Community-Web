from community.web.models import UserProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_profile import UserProfileSerializer
from rest_framework import viewsets

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer