from lib2to3.pgen2 import token
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.custom_validators import check_empty
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


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


class PasswordUpdateSerializer(serializers.Serializer):
    old_pass = serializers.CharField(write_only=True, required=True)
    new_pass = serializers.CharField(write_only=True, required=True)
    new_pass1 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['old_pass', 'new_pass', 'new_pass1']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return value
    
    def validate(self, attrs):
        if attrs['new_pass'] != attrs['new_pass1']:
            raise serializers.ValidationError({'new_pass1': "The two password fields didn't match."})
        self.validate_old_password(attrs['old_pass'])
        password_validation.validate_password(attrs['new_pass'], self.context['request'].user)

        return attrs
    
    def save(self, **kwargs):
        password = self.validated_data['new_pass']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=5, required=True)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs['email']
        if(User.objects.filter(email = email).exists()):
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user=user)
            current_site = get_current_site(self.context['request']).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            abs_url = "http://" + current_site + relative_link 
            email_html = render_to_string('api_email_template.html', {'user':user, 'abs_url':abs_url,' current_site':current_site})
            email_body = strip_tags(email_html)
            data = {
                'body':email_body,
                'to':email,
                'subject':"Reset Email" + f" {current_site}",
                'html_message':email_html,
            }
            subject = "Reset Email" + f" {current_site}"

            send_mail(subject, email_body,  settings.EMAIL_HOST_USER, [email], html_message=email_html, fail_silently=True)
        else:
            raise serializers.ValidationError("User with this email does not exists.")

        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True,min_length=5,required=True)
    token = serializers.CharField(write_only=True,min_length=10,required=True)
    uidb64 = serializers.CharField(write_only =True, min_length=1,required=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        print("asdakhdkajgdjak,dg")
        id = force_str(urlsafe_base64_decode(attrs.get("uidb64")))
        token = attrs['token']
        password = attrs['password']
        try:
            user = User.objects.get(id = id)
        except:
            raise serializers.ValidationError("user with id not exist try password reset after sometime")
        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise AuthenticationFailed("Please enter valid credentiails or try resetting after sometime")
        password_validation.validate_password(password, user)


        return attrs



    def save(self, **kwargs):
        id = force_str(urlsafe_base64_decode(self.validated_data.get("uidb64")))
        user = User.objects.get(id=id)
        print("pavan")
        user.set_password(self.validated_data['password'])
        user.save()
        return user
