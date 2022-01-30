from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from base.models import Topic
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserForm
# Create your views here.


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
            return render(request, 'accounts/login_register.html', {})    
            
        
        user = authenticate(request, email = email, password = password)
        if(user is not None):
            login(request, user)
            messages.success(request, "Login success")
            return redirect('base:home')
        else:
            messages.error(request, "username and password does not match")

    context = {'page':page}
    return render(request, 'accounts/login_register.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "Logout success")
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
    return render(request, 'accounts/login_register.html', context)


@login_required
def update_user_view(request):

    if(request.method == 'POST'):
        form = UserForm(request.POST,request.FILES,  instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.id)
        else:
            messages.warning(request, "something went wrong")

    user = request.user
    form = UserForm(instance=user)
    context = {'form':form, 'user':user}

    return render(request, 'accounts/update_user.html', context)

def profile_view(request, pk):
    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()
    topics_count = Topic.objects.count()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()[:5]
    context = {'user':user,'rooms':rooms, 'room_messages':room_messages, 'topics':topics, 'topics_count' : topics_count}
    return render(request, 'accounts/profile.html', context)
