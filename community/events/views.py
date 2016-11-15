from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,template_name='events/home.html')

def create_events(request):
    return render(request, template_name='events/create_events.html')

