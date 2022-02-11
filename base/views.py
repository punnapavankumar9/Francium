from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import Request, Room, Topic , Message
from base.forms import MessageForm, RoomForm
from api.custom_validators import check_empty
# Create your views here.

# rooms = [
#     {'id':1, 'info':'this is about c++'},
#     {'id':2, 'info':'learn C# buddy'},
#     {'id':3, 'info':'please teach Kotlin'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(
                Q(topic__name__icontains = q) | 
                Q(name__icontains = q)|
                Q(description__icontains = q)
            ).order_by("-updated")
    room_count = rooms.count()
    paginator = Paginator(rooms, 2)
    page_number = request.GET.get('page')
    # if(page_number is not None)
    rooms = paginator.get_page(page_number)
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q) & Q(room__is_private=False))[:5]
    topics_count = Topic.objects.count()
    topics = Topic.objects.all()[:5]
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages, 'topics_count':topics_count}
    # messages.info(request, "dsd adsa adsd asd ads")
    return render(request, 'base/home.html', context)


def about(request):
    return render(request, 'base/about.html')

def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    if(room.is_private == False or room.participants.filter(id=request.user.id).exists()):
        form = MessageForm()
        if(request.method == 'POST'):
            body = request.POST.get('msg_body')
            form = MessageForm(request.POST, request.FILES)
            if(form.is_valid() and (not check_empty(body) or request.FILES.get('message_image') is not None)):
                message = form.save(commit=False)
                if(message.message_image != "messages/default.jpg"):
                    message.isImage = True
                    message.body = message.message_image.name
                else:
                    message.body = body
                message.user = request.user
                message.room = room
                message.save()
                room.participants.add(request.user)
                return redirect('base:room', pk=room.id)
            else:
                messages.error(request, form.errors)
            # pass
            # msg = Message.objects.create(
            #     user = request.user,
            #     body = body,
            #     room = room
            # )

        room_messages = room.message_set.all().order_by('-created')[:10][::-1]
        participants = room.participants.all()
        context = {'has_access':True, 'room':room, 'msgs':room_messages, 'participants':participants, 'form':form}
        return render(request, 'base/room.html', context)
    else:
        if not request.user.is_authenticated:
            messages.info(request, "This room is private you must login to view this")
            return redirect("accounts:login")

        if(request.method == "POST"):
            req , created = Request.objects.get_or_create(
                user = request.user,
                room = room,
            )
        requested = Request.objects.filter(user=request.user, room=room)
        if(requested.exists()):
            requested = True
        else:
            requested = False
        context = {"has_access":False, 'room':room, 'requested':requested}
        return render(request, 'base/room.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host = request.user,
            topic = topic,
            name=request.POST.get('name'),
            description = request.POST.get('description')
        )
        if(request.POST.get('is_private') == 'on'):
            room.is_private = True
        room.save()
        room.participants.add(request.user)
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
    if(request.user != room.host):
        return HttpResponse("Your are not allowed here!")

    form = RoomForm(instance=room)
    if(request.method == 'POST'):
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        if(request.POST.get('is_private') == 'on'):
            room.is_private = True
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


@login_required
def delete_message(request, pk):
    msg = get_object_or_404(Message, id=pk)
    if(request.user  != msg.user):
        return HttpResponse("Your are not allowed here!")
    if(request.method == 'POST'):
        msg.delete()
        return redirect('base:home')
    return render(request, 'base/forms/delete.html', {'obj':msg})



def topics_view(request):


    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}

    return render(request, 'base/topics.html', context)


def activity_view(request):
    room_messages = Message.objects.filter(Q(room__is_private=False))
    paginator = Paginator(room_messages, 5)
    page_number = request.GET.get('page')
    room_messages = paginator.get_page(page_number)
    context = {'room_messages':room_messages}
    
    return render(request, 'base/activity.html', context)

def room_requests(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if(room.host != request.user):
        return HttpResponse("You are not Allowed Here")
    

    join_requests = room.request_set.all()
    if request.method == 'POST':
        for req in join_requests:
            if(request.POST.get(req.user.username) == 'Accept'):
                room.participants.add(req.user)
                req.delete()
            elif(request.POST.get(req.user.username) == 'Decline'):
                req.delete()
        return redirect('base:room' , pk=room.id)

    context = {'join_requests':join_requests}
    
    return render(request, 'base/room_requests.html', context)