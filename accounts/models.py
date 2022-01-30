from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null = True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True,upload_to="profile_pics/", default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
