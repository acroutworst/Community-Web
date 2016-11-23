from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Community, CommunityUserProfile
from .forms import CreateCommunityProfileForm


@login_required
def communities_list(request):
    communities = Community.objects.all()
    context = {
        'communities': communities
    }
    return render(request, template_name='communities/list.html', context=context)


@login_required
def communities_view(request, slug):
    if slug is None:
        HttpResponseRedirect('/communities/')
    community = Community.objects.filter(slug=slug)
    user = request.user
    if community.count() == 0:
        HttpResponseRedirect('/communities/')
    profile = CommunityUserProfile.objects.filter(user=user, community=community).first()
    context = {
        'community': community.first(),
        'user': user,
        'member': profile,
    }
    return render(request, template_name='communities/view.html', context=context)


@login_required
def communities_join(request, slug):
    if slug is None:
        HttpResponseRedirect('/communities/')
    community = Community.objects.get(slug=slug)
    user = request.user
    profile = CommunityUserProfile.objects.filter(user=user, community=community).first()
    if profile:
        if profile.active:
            return HttpResponseRedirect('/communities/' + slug)
        else:
            if request.method == 'POST':
                profile.active = True
                profile.save()
                return HttpResponseRedirect('/communities/' + slug)
            elif request.method == 'GET':
                return render(request, template_name='communities/reactivate.html', context={'community': community})
    else:
        profile = CommunityUserProfile()
        profile.community = community
        profile.user = user
        if request.method == 'POST':
            form = CreateCommunityProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/communities/' + slug)
        elif request.method == 'GET':
            form = CreateCommunityProfileForm(instance=profile)
        else:
            return HttpResponseRedirect('/communities/' + slug)
    context = {
        'user': user,
        'community': community,
        'form': form,
    }
    return render(request, template_name='communities/join.html', context=context)


@login_required
def communities_deactivate(request, slug):
    community = Community.objects.get(slug=slug)
    user = request.user
    profile = CommunityUserProfile.objects.get(user=user, community=community)
    if not profile.active:
        return HttpResponseRedirect('/communities/' + slug)
    if request.method == 'POST':
        profile.active = False
        profile.save()
        return HttpResponseRedirect('/communities/' + slug)
    context = {
        'user': user,
        'community': community,
    }
    return render(request, template_name='communities/deactivate.html', context=context)

@login_required
def communities_profile(request, slug):
    if slug is None:
        HttpResponseRedirect('/communities/')
    community = CommunityUserProfile.objects.filter(slug=slug).first()
    user = request.user
    department = CommunityUserProfile.objects.values_list('department', flat = True).get(user=user, community=community)
    position = CommunityUserProfile.objects.values_list('position', flat=True).get(user=user, community=community)
    if community.count() == 0:
        HttpResponseRedirect('/communities/')
    profile = CommunityUserProfile.objects.get(user=user, community=community).first()





    if not profile.active:
        return HttpResponseRedirect('/communities/' + slug)
    if request.method == 'POST':
        profile.active = False
        profile.save()
        return HttpResponseRedirect('/communities/' + slug)

    context = {
        'community': community.first(),
        'user': user,
        'department': department,
        'position':position,
    }
    return render(request, template_name='communities/community_profile.html', context=context)
