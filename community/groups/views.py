
from django.contrib.auth.decorators import login_required
from community.groups.models import Group
from community.communities.models import Community
from community.groups.form import CreateGroupForm
import datetime
from django.shortcuts import render, redirect


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
#def groups_view (request, slug, id):
def groups_view (request, id):
    #community = Community.objects.get(slug=slug)
    groups = Group.objects.filter(id = id)

    user = request.user
    context = {
        'user': user,
        #'community': community,
        'group': groups,

    }

    return render(request, template_name= 'groups/view.html', context = context)

@login_required
def group_create(request):
    #community = Community.objects.get(slug=slug)

    form = CreateGroupForm
    user = request.user

    if request.method == 'POST':
       # group = Group(community=community, creat_by =user,create_date=datetime.datetime.now())
        group = Group(create_by=user, create_date=datetime.datetime.now())
        form = CreateGroupForm(request.POST, request.FILES, instance=group)
        form.save()
        return redirect ('groups_view', id=group.id)
    context = {
        #'community': community,
        'user': user,
        'form': form,
    }

    return render (request, template_name='groups/create.html', context=context)




