from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from community.communities.models import Community

# Create your views here.
def chatroom_view(request):
    return render(request,'chatroom/chatroom.html')

@login_required
def chatroom_user(request, slug):
    community = Community.objects.get(slug=slug)

    context = {
        'community': community.title,
        'user': request.user.username,
    }
    return render(request, template_name='chatroom/chatroom.html', context=context)