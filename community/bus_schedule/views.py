from django.shortcuts import render

# Create your views here.
def bus_schedule_view(request):
    return render(request,'bus_schedule/bus_schedule.html')