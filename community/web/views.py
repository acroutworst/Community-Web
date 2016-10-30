from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.utils.six import BytesIO
from community.rest_api import serializers, views as api_views
from rest_framework.renderers import JSONRenderer
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def list_groups(request):
    #api_views.group.GroupViewSet
    #group_serializer = serializers.group.GroupSerializer(response)
    #groups = JSONRenderer().render(group_serializer.data)
    groups = Group.objects.all().order_by('-name')
    return render(request, 'groups/list.html', {'groups': groups})