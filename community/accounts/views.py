from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Profile, ProfileImage
from .forms import ProfileEditForm, ProfileImageUploadForm
from allauth.account.models import EmailAddress
from django.http import HttpResponseRedirect
from community.communities.models import CommunityUserProfile
from community.meetups.models import Attendee, Meetup

# @login_required
# def profile_view(request):
#     return profile_view(request, userid=request.user)

@login_required
def profile_view(request, userid=None):
    profile_user = request.user
    if userid:
        profile_user = User.objects.get(id=userid)
    profile_query = Profile.objects.filter(user=profile_user)
    email_query = EmailAddress.objects.filter(user=profile_user)
    if profile_query.count() == 0:
        profile = Profile.objects.create(user=profile_user)
    else:
        profile = Profile.objects.get(user=profile_user)
    attending = Attendee.objects.exclude(status=Attendee.STATUS_CHOICES[3][0]).filter(user=profile_user)
    meetups = Meetup.objects.filter(attendee__in=attending, active=True)
    memberships = CommunityUserProfile.objects.filter(user=profile_user, active=True)
    context = {
        'profile': profile,
        'profile_user': profile_user,
        'current_user': request.user,
        'memberships': memberships,
        'meetups': meetups,
    }
    return render(request, 'accounts/profile/view.html', context)

@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile/')
    elif request.method == 'GET':
        form = ProfileEditForm(instance=profile)
    else:
        return HttpResponseRedirect('/accounts/profile/')

    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile/edit.html', context)

@login_required
def profile_image_upload(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = ProfileImage.objects.create(profile=profile,
                                                image=form.cleaned_data['image']
                                                )
            profile.image = image
            image.save()
            profile.save()
            return HttpResponseRedirect('/accounts/profile')
    elif request.method == 'GET':
        form = ProfileImageUploadForm
    else:
        return HttpResponseRedirect('/accounts/profile')
    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile/imageupload.html', context)