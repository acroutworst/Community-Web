from django.shortcuts import render
from .models import Meetup, MeetupAttendee



def meetups_list(request):
    meetups = Meetup.objects.all()
    context = {
        'meetups': meetups,
        'user': request.user,
    }
    return render(request, template_name='meetups/list.html', context=context)