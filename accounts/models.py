from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from base.resize_image import ResizeImageMixin
# Create your models here.
class User(AbstractUser, ResizeImageMixin):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True, null = True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True,upload_to="profile_pics/", default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.avatar != "avatar.svg":
            self.resize(self.avatar, (300, 300))
        super().save(*args, **kwargs)
