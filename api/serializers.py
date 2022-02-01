from rest_framework import serializers
from base.models import Room


class RoomSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(read_only = True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'