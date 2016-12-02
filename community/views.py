import operator
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .communities.models import Community, CommunityUserProfile
from .meetups.models import Meetup

from django.db.models import Q



def home(request):
    if request.user.is_authenticated:
        return home_login(request)
    else:
        context = {

        }
        return render(request, template_name='index_1.html')#context=context)


@login_required
def home_login(request):
    all_communities = Community.objects.all()
    my_communities = Community.objects.filter(communityuserprofile__user=request.user)
    meetup_list = Meetup.objects.filter(community__in=my_communities, active=True)
    context = {
        'user': request.user,
        'all_communities': all_communities,
        'my_communities': my_communities,
        'meetup_list': meetup_list,
    }
    return render(request, template_name='index_user.html', context=context)

