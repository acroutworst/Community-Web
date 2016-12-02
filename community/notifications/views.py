from django.shortcuts import render

from .models import Notification

# Create your views here.
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:10]
    context = {
        'notifications_list': notifications
    }
    return render(request, 'notifications/view.html', context)