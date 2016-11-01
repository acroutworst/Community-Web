from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render
from .models import UserProfile
from .forms import ProfileEditForm
from allauth.account.models import EmailAddress
from django.http import HttpResponseRedirect

@login_required
def profile_view(request):
    user = request.user
    profileQuery = UserProfile.objects.filter(user=user)
    emailQuery = EmailAddress.objects.filter(user=user)
    if profileQuery.count() == 0:
        profile = UserProfile.objects.create(user=user)
    else:
        profile = UserProfile.objects.get(user=user)
    context = {
        'profile': profile,
        'user': user,
        'emails': emailQuery,
    }
    return render(request, 'accounts/profile/view.html', context)

@login_required
def profile_edit(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form = ProfileEditForm(instance=profile)
    context = {
        'user': user,
        'profile': profile,
        'form': form,
    }
    return render(request, 'accounts/profile/edit.html', context)
