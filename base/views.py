from asyncio.windows_events import NULL
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.template import context
from base.models import Room, Topic , Message
from base.forms import RoomForm
# Create your views here.

# rooms = [
#     {'id':1, 'info':'this is about c++'},
#     {'id':2, 'info':'learn C# buddy'},
#     {'id':3, 'info':'please teach Kotlin'},
# ]

def home(request):

    q= request.GET.get('q') if request.GET.get('q') != None else ""

    rooms = Room.objects.filter(
                Q(topic__name__icontains = q) | 
                Q(name__icontains = q)|
                Q(description__icontains = q)
            )

    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count':rooms.count(), 'room_messages':room_messages}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')

def profile_view(request, pk):
    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()

    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

def room(request, pk):
    room = get_object_or_404(Room, id=pk)

    if(request.method == 'POST'):
        msg = Message.objects.create(
            user = request.user,
            body = request.POST.get('msg_body'),
            room = room
        )
        room.participants.add(request.user)
        return redirect('base:room', pk=room.id)

    room_messages = room.message_set.all()
    participants = room.participants.all()
    context = {'room':room, 'msgs':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('base:home')

    form = RoomForm()
    context = {'form': form}
    return render(request, 'base/forms/room.html', context)

def update_room(request, pk):
    room = get_object_or_404(Room, id = pk)
    form = RoomForm(instance=room)

    if(request.user != room.host):
        return HttpResponse("Your are not allowed here!")


    if(request.method == 'POST'):
        form = RoomForm(request.POST or None , instance=room)
        if(form.is_valid()):
            form.save()
            return redirect('base:home')
    context = {'form':form}

    return render(request, 'base/forms/room.html', context)    


def delete_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if(request.user != room.host):
        return HttpResponse("Your are not allowed here!")
    if(request.method == 'POST'):
        room.delete()
        return redirect('base:home')
    
    context = {'obj' :room}
    return render(request, 'base/forms/delete.html',context)

def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:home')

    if(request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            temp_user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists")
            return render(request, 'base/forms/login_register.html', {})    
            
        
        user = authenticate(request, username = username, password = password)
        if(user is not None):
            login(request, user)
            messages.success(request, "Login success")
            return redirect('base:home')
        else:
            messages.error(request, "username and password does not match")

    context = {'page':page}
    return render(request, 'base/forms/login_register.html', context)

def logout_view(request):
    logout(request)
    return redirect('base:home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('base:home')
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, "An error occured during registration")


    context = {'page':page, 'form':form}
    return render(request, 'base/forms/login_register.html', context)

@login_required
def delete_message(request, pk):
    msg = get_object_or_404(Message, id=pk)
    if(request.user  != msg.user):
        return HttpResponse("Your are not allowed here!")
    if(request.method == 'POST'):
        msg.delete()
        return redirect('base:home')
    return render(request, 'base/forms/delete.html', {'obj':msg})
