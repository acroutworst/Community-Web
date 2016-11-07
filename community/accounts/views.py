from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Profile
from .forms import ProfileEditForm
from allauth.account.models import EmailAddress
from django.http import HttpResponseRedirect, QueryDict

@login_required
def profile_view(request):
    profile_user = request.user
    profile_query = Profile.objects.filter(user=profile_user)
    email_query = EmailAddress.objects.filter(user=profile_user)
    if profile_query.count() == 0:
        profile = Profile.objects.create(user=profile_user)
    else:
        profile = Profile.objects.get(user=profile_user)
    context = {
        'profile': profile,
        'current_user': profile_user,
        'emails': email_query,
    }
    return render(request, 'accounts/profile/view.html', context)

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
    context = {
        'profile': profile,
        'profile_user': profile_user,
        'emails': email_query,
        'current_user': request.user,
    }
    return render(request, 'accounts/profile/view.html', context)

@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    print('hi')
    print(profile)
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
