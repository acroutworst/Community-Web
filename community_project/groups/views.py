from django.shortcuts import render
from django.contrib.auth.models import Group


def list_groups(request):
    groups = Group.objects.all().order_by('-name')
    return render(request, 'groups/list.html', {'groups': groups})