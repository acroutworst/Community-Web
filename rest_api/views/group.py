from django.contrib.auth.models import Group
from rest_framework import viewsets
from ..serializers import group

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Group.objects.all()
    serializer_class = group.GroupSerializer