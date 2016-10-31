from django.shortcuts import render
from django.contrib.auth.models import Group

# Create your views here.
def list_groups(request):
    #api_views.group.GroupViewSet
    #group_serializer = serializers.group.GroupSerializer(response)
    #groups = JSONRenderer().render(group_serializer.data)
    groups = Group.objects.all().order_by('-name')
    return render(request, 'groups/list.html', {'groups': groups})