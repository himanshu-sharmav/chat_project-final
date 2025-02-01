from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Message
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.cache import cache

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})

@login_required
def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat/index.html', {'users': users})

@login_required
def room(request, username):
    other_user = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    return render(request, 'chat/room.html', {
        'other_user': other_user,
        'users': users,
        'messages': messages
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def online_users(request):
    online_users = cache.get('online_users', set())
    users = User.objects.filter(username__in=online_users)
    return render(request, 'chat/online_users.html', {'users': users})