from django.contrib import admin
from .models import Room, Topic, Message, Request

# Register your models here.

class AdminRoom(admin.ModelAdmin):
    list_display = ['name', 'topic', 'is_private']

class AdminRequest(admin.ModelAdmin):
    pass


admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Room , AdminRoom)
admin.site.register(Request , AdminRequest)