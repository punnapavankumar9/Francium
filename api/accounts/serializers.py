from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

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



