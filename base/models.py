from distutils.command.upload import upload
from email.policy import default
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from base.resize_image import ResizeImageMixin

# Create your models here.

User = get_user_model()

class Topic(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self) -> str:
        return self.name

class Message(models.Model, ResizeImageMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    isImage = models.BooleanField(default=False)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    message_image = models.ImageField(default="messages/default.jpg", upload_to="messages/", null=True, blank=True)

    def __str__(self) -> str:
        if(len(self.body) > 50):
            return self.body[0:50]
        return self.body
    
    # def save(self, *args, **kwargs):
    #     if self.message_image:
    #         self.resize(self.message_image, (300, 300))
    #     super().save(self, *args, **kwargs)

    class Meta:
        ordering = ['-updated', '-created']


