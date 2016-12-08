
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from community.groups.models import Group, GroupMembers
from community.communities.models import Community
from community.groups.form import CreateGroupForm #, JoinGroupForm
import datetime
from django.shortcuts import render, redirect


@login_required
def groups_list(request, slug):
    community = Community.objects.get(slug=slug)
    groups = Group.objects.filter(community=community)
    user = request.user

    context = {
        'community':community,
        'groups': groups,
        'user': user,
    }


    return render(request, template_name='groups/list.html', context=context)

@login_required
#def groups_view (request, slug, id):
def groups_view (request, slug, id):
    community = Community.objects.get(slug=slug)
    groups = Group.objects.get(community=community, id = id)
    member = GroupMembers.objects.filter(group=groups).first()
    active_member = GroupMembers.objects.exclude(active=False).filter(group=groups)

    user = request.user
    context = {
        'user': user,
        'community':community,
        'group': groups,
        'members':member,
        'active_members':active_member,

    }

    return render(request, template_name= 'groups/view.html', context = context)

@login_required
def group_create(request,slug):
    community = Community.objects.get(slug=slug)

    form = CreateGroupForm
    user = request.user

    if request.method == 'POST':
       # group = Group(community=community, creat_by =user,create_date=datetime.datetime.now())
        group = Group(community=community, create_by=user, create_date=datetime.datetime.now())
        form = CreateGroupForm(request.POST, request.FILES, instance=group)
        form.save()
        return redirect ('groups_view', id=group.id)
    context = {
        'community': community,
        'user': user,
        'form': form,
    }

    return render (request, template_name='groups/create.html', context=context)

@login_required
def group_join(request,slug, id):
    if id is None:
        HttpResponseRedirect('/groups/')
    group = Group.objects.get(id=id)
    user=request.user
    community=Community.objects.get(slug=slug)
    member=GroupMembers.objects.filter(community=community,user=user,group=group).first()
    if member:
        if member.active:
            return HttpResponseRedirect('/greops/' + id)
        else:
            if request.method == 'POST':
                    member.active=True
                    member.save()
                    return HttpResponseRedirect('/groups/' + id)

    else:

        member = GroupMembers()#user=user,group=group,join_date=datetime.datetime.now())
        member.community=community
        member.user=user
        member.group=group
        member.join_date=datetime.datetime.now()
        if request.method == 'POST':
            member.active=True
            member.save()
            #form = JoinGroupForm(request.POST, request.FILES,instance=member)
            #form.save()
            return HttpResponseRedirect('/groups/' + id)

    context = {
        'user': user,
        'group': group,
        'member': member,
        'community':community,

    }
    return render(request, template_name='groups/join.html', context=context)

@login_required
def group_deactivate (request,slug, id):
    group = Group.objects.filter(id=id).first()
    user = request.user
    community=Community.objects.get(slug=slug)
    member = GroupMembers.objects.get(user=user,group=group)
    if not member.active:
        return HttpResponseRedirect('/groups/' +id)
    if request.method=='POST':
        member.active=False
        member.save()
        return HttpResponseRedirect('/groups/' + id)
    context = {
        'user':user,
        'group':group,
        'member':member,
        'community':community,
    }
    return render(request, template_name='groups/deactivate.html',context=context)

@login_required
def group_member_view (request,slug, id):
    community=Community.objects.get(slug=slug)
    group = Group.objects.filter(id=id).first()
    user=request.user
    member = GroupMembers.objects.filter(group = group)
    context = {
        'community':community,
        'group': group,
        'user':user,
        'members':member,
    }
    return render(request,template_name='groups/member.html',context=context)






