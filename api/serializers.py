from rest_framework import serializers
from api.custom_validators import check_empty
from base.models import Room, Message, Topic, Request

class RoomSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(read_only = True)
    created = serializers.DateTimeField(read_only=True)
    topic = serializers.CharField(max_length = 200)
    class Meta:
        model = Room
        fields = ['host', 'name', 'description','topic', 'participants',  'is_private', 'created', 'updated',]
        extra_kwargs = {
            'topic':{'required':True},
            'name':{'required':True},
            'is_private':{'required':True},
            'participants':{'read_only':True},
        }
    def validate(self, attrs):
        super().validate(attrs)
        error = {}
        for i in ['name', 'topic']:
            if(check_empty(attrs[i])):
                error['error'] = "please provide valid " + i
                raise serializers.ValidationError(detail=error)
        return attrs

class MessageSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only = True)
    updated = serializers.DateTimeField(read_only = True)
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    isImage = serializers.BooleanField(read_only=True)
    message_image = serializers.ImageField(required=False)

    class Meta:
        model = Message
        fields = ['user', 'room', 'isImage', 'body', 'updated', 'created', 'message_image']

        extra_kwargs = {
            'room':{'required':False},
        }
    

class TopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = "__all__"

        extra_kwargs = {
            'name':{'required':False},
        }

class UserRoomRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['user','room', 'request_time']
        extra_kwargs = {
            'request_time':{'read_only':True},
            'user':{'read_only':True},
            'room':{'required':True}
        }