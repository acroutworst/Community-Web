from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from community.communities.models import Group,Group_Members
from community.communities.models import Community

@login_required
def list_groups(request, slug):
    community = Community.objects.get(slug = slug)
    groups = Group.objects.filter (community = community)
    user = request.user
    context = {
        'community': community,
        'groups': groups,
        'user': user,
    }


    return render(request, 'groups/list.html', context = context)

@login_required
def view_group (request, slug, id):
    community = Community.objects.get(slug=slug)
    groups = Group.objects.filter(community=community, id = id)
    group_member = Group_Members.objects.filter(community = community, group = groups)
    user = request.user
    context = {
        'user': user,
        'community': community,
        'group': groups,
        'group_members': group_member,
    }

    return render(request, 'group/view.html', context = context)
