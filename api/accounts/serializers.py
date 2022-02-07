from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from api.custom_validators import check_empty

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','username', 'email', 'password',]
        extra_kwargs = {
            'name':{'required':True},
            'password':{'write_only':True},
            'email':{'required':True},
        }
    def create(self, validated_data):
        error = {}
        for i in validated_data:
            if(check_empty(validated_data[i])):
                error['error'] = "please provide valid " + i
                raise serializers.ValidationError(detail=error)
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email','bio','avatar', 'first_name', 'last_name', 'date_joined',]

    def update(self, instance, validated_data):
        error = {}
        if(len(validated_data) == 0):
            error['error'] = "please provide some fields to modify"
            raise serializers.ValidationError(detail=error)
        for i in validated_data:
            if(check_empty(validated_data[i])):
                error['error'] = "please provide valid " + i
                raise serializers.ValidationError(detail=error)
        return super().update(instance, validated_data)

    