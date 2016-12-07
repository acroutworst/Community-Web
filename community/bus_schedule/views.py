from django.shortcuts import render

# Create your views here.
def bus_schedule(request):
    return render(request,'bus_schedule/bus_schedule.html')