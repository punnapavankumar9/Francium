from importlib.metadata import requires
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from base.models import Room, Topic , Message, User
from base.forms import RoomForm, UserForm, CustomUserCreationForm
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

    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))[:5]
    topics_count = Topic.objects.count()
    topics = Topic.objects.all()[:5]
    context = {'rooms':rooms, 'topics':topics, 'room_count':rooms.count(), 'room_messages':room_messages, 'topics_count':topics_count}
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')

def profile_view(request, pk):
    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()
    topics_count = Topic.objects.count()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()[:5]
    context = {'user':user,'rooms':rooms, 'room_messages':room_messages, 'topics':topics, 'topics_count' : topics_count}
    return render(request, 'base/profile.html', context)

def room(request, pk):
    room = get_object_or_404(Room, id=pk)

    if(request.method == 'POST'):
        body = request.POST.get('msg_body')
        flag = False
        if(body is None or body == ""):
            flag = True
        if(not flag):
            msg = Message.objects.create(
                user = request.user,
                body = body,
                room = room
            )
            room.participants.add(request.user)
            return redirect('base:room', pk=room.id)

    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    context = {'room':room, 'msgs':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name=request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('base:home')


        # if(form.is_valid()):
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     form.save()
        #     return redirect('base:home')

    form = RoomForm()
    topics = Topic.objects.all()
    context = {'form': form, 'topics':topics}
    return render(request, 'base/forms/room.html', context)

def update_room(request, pk):
    room = get_object_or_404(Room, id = pk)
    form = RoomForm(instance=room)

    if(request.user != room.host):
        return HttpResponse("Your are not allowed here!")


    if(request.method == 'POST'):
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('base:home')

        # form = RoomForm(request.POST or None , instance=room)
        # if(form.is_valid()):
        #     form.save()
        #     return redirect('base:home')
    topics = Topic.objects.all()
    
    context = {'form':form, 'topics':topics, 'room':room}

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
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            temp_user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exists")
            return render(request, 'base/forms/login_register.html', {})    
            
        
        user = authenticate(request, email = email, password = password)
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
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
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


@login_required
def update_user_view(request):

    if(request.method == 'POST'):
        form = UserForm(request.POST,request.FILES,  instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('base:profile', request.user.id)
        else:
            messages.warning(request, "something went wrong")

    user = request.user
    form = UserForm(instance=user)
    context = {'form':form, 'user':user}

    return render(request, 'base/forms/update_user.html', context)

def topics_view(request):


    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}

    return render(request, 'base/topics.html', context)


def activity_view(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    
    return render(request, 'base/activity.html', context)