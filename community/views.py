import operator
import re
import feedparser

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .communities.models import Community, CommunityUserProfile
from .meetups.models import Meetup
from .notifications.models import Notification

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
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:2]
    feed = feedparser.parse('https://www.uwb.edu/news?rss=blogs')
    entries = feed.entries
    num_entries = 5
    context = {
        'user': request.user,
        'all_communities': all_communities,
        'my_communities': my_communities,
        'community': all_communities.first(),
        'meetup_list': meetup_list,
        'notifications_list': notifications,
        'feed': feed,
        'entries': entries,
        'num_entries': num_entries,
    }
    return render(request, template_name='dashboard.html', context=context)

