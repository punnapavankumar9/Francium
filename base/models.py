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
    is_private = models.BooleanField(default=False)

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

    class Meta:
        ordering = ['-updated', '-created']


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    request_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-request_time', 'room']
        verbose_name = 'Join request'
    
    def __str__(self) -> str:
        return self.user.username + " requested to join " + self.room.name

    




