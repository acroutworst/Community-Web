from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from community.groups.models import Group,GroupMembers
from community.communities.models import Community

@login_required
def groups_list(request):
    groups = Group.objects.all()
    user = request.user
    context = {

        'groups': groups,
        'user': user,
    }


    return render(request, template_name='groups/list.html', context=context)

@login_required
def groups_view (request, slug, id):
    community = Community.objects.get(slug=slug)
    groups = Group.objects.filter(community=community, id = id)
    group_member = GroupMembers.objects.filter(community = community, group = groups)
    user = request.user
    context = {
        'user': user,
        'community': community,
        'group': groups,
        'group_members': group_member,
    }

    return render(request, template_name= 'group/view.html', context = context)
