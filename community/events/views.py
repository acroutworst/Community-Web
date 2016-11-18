from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event


def index(request):
    return render(request,template_name='events/home.html')

def create_events(request):
    if request.method == "POST":
        event = Event()
        query = request.POST
        event.firstname = query['firstname']
        event.lastname = query['lastname']
        event.email = query['email']
        event.start_time = query['start_time']
        event.end_time = query['end_time']

        if query['event_type'] == 'Private':
            event.private = True
        else:
            event.private = False
        event.save()
        return view_event(request, event)
    return render(request, template_name='events/create_events.html')

def view_event(request, event=None):
    context = {}
    if event != None:
         context['event']=event
    return render(request, template_name='events/view_event.html', context=context)

