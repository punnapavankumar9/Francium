from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import User
from base.models import Topic
from django.db.models import Q
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm, UserForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.core.paginator import Paginator
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

def login_view2(request, from_password_reset):
    from_login = request.GET.get('from_password_reset') if request.GET.get('from_password_reset') != None else 0
    auth_tagline = ""
    if(from_login):
        auth_tagline = "Your password has been set.  You may go ahead and log in now."
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

    context = {'page':page, 'auth__tagline': auth_tagline}
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
            messages.error(request, form.errors)


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
            messages.warning(request, form.errors)

    user = request.user
    form = UserForm(instance=user)
    context = {'form':form, 'user':user}

    return render(request, 'accounts/update_user.html', context)

def profile_view(request, pk):
    user = get_object_or_404(User, id=pk)
    if(request.user.id == int(pk)):
        rooms = user.room_set.all()
    else:
        rooms = user.room_set.filter(is_private=False)
    topics_count = Topic.objects.count()
    room_messages = user.message_set.filter(Q(room__is_private=False))[:5]
    topics = Topic.objects.all()[:5]
    context = {'user':user,'rooms':rooms, 'room_messages':room_messages, 'topics':topics, 'topics_count' : topics_count}
    return render(request, 'accounts/profile.html', context)

# password reset class

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    post_reset_login = True
    success_url = reverse_lazy('accounts:login', kwargs={'from_password_reset':1})

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


