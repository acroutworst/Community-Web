from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Meetup, Attendee
from community.communities.models import Community
from .forms import CreateMeetupForm, AttendMeetupForm
from django.utils import timezone
import datetime


@login_required
def community_meetups_list(request, slug):
    community = Community.objects.get(slug=slug)
    meetups = Meetup.objects.filter(community=community, active=True)
    attendees = Attendee.objects.filter(meetup__community=community)
    context = {
        'community': community,
        'meetups': meetups,
        'attendees': attendees,
        'user': request.user,
    }
    return render(request, template_name='meetups/list_community.html', context=context)

@login_required
def user_meetups_list(request, user_id=None):
    if not user_id:
        user = request.user
    else:
        user = User.objects.get(id=user_id)
    meetups = Meetup.objects.filter(attendee__user=user, active=True)
    meetup_history = Meetup.objects.filter(attendee__user=user, active=False)
    attendees = Attendee.objects.filter(meetup__in=meetups)
    context = {
        'meetups': meetups,
        'attendees': attendees,
        'user': user,
        'current_user': request.user,
        'meetup_history': meetup_history,
    }
    return render(request, template_name='meetups/list_user.html', context=context)


@login_required
def meetups_view(request, slug, id):
    community = Community.objects.get(slug=slug)
    meetup = Meetup.objects.get(community=community, id=id)
    attendees = Attendee.objects.exclude(status=Attendee.STATUS_CHOICES[3][0]).filter(meetup__community=community, meetup__id=id)
    user = request.user
    my_rsvp = Attendee.objects.filter(meetup=meetup, user=user).first()
    if my_rsvp is not None and my_rsvp.status is not 'NOT_GOING':
        attending = True
    else:
        attending = False
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
        meetup = Meetup(community=community, creator=user, created_date=timezone.now())
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


@login_required()
def meetup_change_status(request, slug, id):
    user = request.user
    community = Community.objects.get(slug=slug)
    meetup = Meetup.objects.get(community=community, id=id)
    try:
        attendee = Attendee.objects.get(user=user, meetup=meetup)
    except Attendee.DoesNotExist:
        return redirect('meetups_view', slug=slug, id=meetup.id)
    if request.method == 'POST':
        form = AttendMeetupForm(request.POST, request.FILES, instance=attendee)
        if form.is_valid():
            form.save()
            return redirect('meetups_view', slug=slug, id=meetup.id)
    elif request.method == 'GET':
        form = AttendMeetupForm(instance=attendee)
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
    if meetup.max_attendees and meetup.max_attendees <= Attendee.objects.exclude(status=Attendee.STATUS_CHOICES[3][0]).filter(meetup=meetup).count():
        return False
    start_time = meetup.created_date
    end_time = start_time + datetime.timedelta(hours=meetup.duration)
    if datetime.datetime.now().utcnow() > end_time.utcnow():
        return False
    return True

