from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterUserSerializer
from django.contrib.auth.hashers import make_password


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
            token, created = Token.objects.get_or_create(user = user)
            data['token'] = token.key
            return Response(data)
        else:
            data = serializer.errors
        return Response(data)