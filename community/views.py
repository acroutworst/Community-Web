from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


def home(request):
    if request.user.is_authenticated:
        return home_login(request)
    else:
        context = {

        }
        return render(request, template_name='index_1.html')#context=context)


@login_required
def home_login(request):
    context = {
        'user': request.user,
    }
    return render(request, template_name='index_user.html', context=context)
