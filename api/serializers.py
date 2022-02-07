from asyncio.windows_events import NULL
from rest_framework import serializers
from api.custom_validators import check_empty
from base.models import Room, Message, Topic

class RoomSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(read_only = True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only = True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    isImage = serializers.ImageField(read_only=True)


    class Meta:
        model = Message
        fields = "__all__"
    
    

class TopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        exclude = []