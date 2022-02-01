from functools import partial
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegisterUserSerializer, UserDetailsUpdateSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token , created = Token.objects.get_or_create(user = user)
        data = {}
        data['username'] = user.username
        data['user_id'] = user.id
        data['token'] = token.key
        data['email'] = user.email
        return Response(data)

@api_view(['POST', ])
def registerUserView(request):
    if request.method == "POST":
        serializer = RegisterUserSerializer(data=request.data)
        data = {}
        if(serializer.is_valid()):
            passwd = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(passwd)
            user = serializer.save()
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.get(user = user)
            data['token'] = token.key
            return Response(data)
        else:
            data = serializer.errors
        return Response(data)

@api_view(['PUT',])
@permission_classes([IsAuthenticated, ])
def updateUserDetailsView(request):
    if request.method == 'PUT':
        serializer = UserDetailsUpdateSerializer(request.user ,data = request.data, partial=True)
        if(serializer.is_valid()):
            user = serializer.save()
            data = {}
            data['message'] = "user details updated"
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors':serializer.errors, 'detail':"fields not updated"}, status=status.HTTP_304_NOT_MODIFIED)