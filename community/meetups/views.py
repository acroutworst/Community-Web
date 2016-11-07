import copy

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Meetup, Attendee
from community.communities.models import Community
from .forms import CreateMeetupForm, AttendMeetupForm
import datetime

@login_required
def meetups_list(request, slug):
    community = Community.objects.get(slug=slug)
    meetups = Meetup.objects.filter(community=community)
    attendees = Attendee.objects.filter(meetup__community=community)
    context = {
        'community': community,
        'meetups': meetups,
        'attendees': attendees,
        'user': request.user,
    }
    return render(request, template_name='meetups/list.html', context=context)


@login_required
def meetups_view(request, slug, id):
    community = Community.objects.get(slug=slug)
    meetup = Meetup.objects.get(community=community, id=id)
    attendees = Attendee.objects.filter(meetup__community=community, meetup__id=id)
    user = request.user
    my_rsvp = Attendee.objects.filter(meetup=meetup, user=user)
    if my_rsvp.count() != 0:
        attending = True
    context = {
        'community': community,
        'meetup': meetup,
        'attendees': attendees,
        'user': user,
        'attending': attending,
        'my_rsvp': my_rsvp,
    }
    return render(request, template_name='meetups/view.html', context=context)


@login_required
def meetups_create(request, slug):
    community = Community.objects.get(slug=slug)
    form = CreateMeetupForm
    user = request.user
    if request.method == 'POST':
        meetup = Meetup(community=community, creator=user, created_date=datetime.datetime.now())
        form = CreateMeetupForm(request.POST, request.FILES, instance=meetup)
        form.save()
        return redirect('meetups_view', slug=slug, id=meetup.id)
    context = {
        'community': community,
        'form': form,
        'user': user,
    }
    return render(request, template_name='meetups/create.html', context=context)


@login_required
def meetups_attend(request, slug, id):
    community = Community.objects.get(slug=slug)
    meetup = Meetup.objects.get(community=community, id=id)
    user = request.user
    form = AttendMeetupForm
    if Attendee.objects.filter(user=user, meetup=meetup).count() != 0:
        return redirect('meetups_view', slug=slug, id=meetup.id)
    if util_meetup_still_open(meetup):
        if request.method == 'POST':
            attendee = Attendee(user=user, meetup=meetup, signup_time=datetime.datetime.now())
            form = AttendMeetupForm(request.POST, request.FILES, instance=attendee)
            if form.is_valid():
                form.save()
                return redirect('meetups_view', slug=slug, id=meetup.id)
    else:
        return redirect('meetups_view', slug=slug, id=meetup.id)

    context = {
        'community': community,
        'meetup': meetup,
        'form': form,
        'user': request.user,
    }
    return render(request, template_name='meetups/attend.html', context=context)



def util_meetup_still_open(meetup):
    if not meetup.active:
        return False
    if meetup.max_attendees and meetup.max_attendees <= Attendee.objects.filter(meetup=meetup).count():
        return False
    start_time = meetup.created_date
    end_time = start_time + datetime.timedelta(hours=meetup.duration)
    if datetime.datetime.now().utcnow() > end_time.utcnow():
        return False
    return True

