from asyncio.windows_events import NULL
from rest_framework import serializers
from api.custom_validators import check_empty
from base.models import Room, Message, Topic

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
        }
    def create(self, validated_data):
        error = {}
        for i in validated_data:
            if(check_empty(validated_data[i])):
                error['error'] = "please provide valid " + i
                raise serializers.ValidationError(detail=error)
        return super().create(validated_data)
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