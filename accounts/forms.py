from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name','username', 'email', 'password1', 'password2',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'name', 'bio',]
