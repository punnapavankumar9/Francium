from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegisterUserSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework import generics


User = get_user_model()
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
def userDetailsView(request, **kwargs):
    if request.method == 'PUT':
        serializer = UserSerializer(request.user ,data = request.data, partial=True)
        if(serializer.is_valid()):
            user = serializer.save()
            data = {}
            data['message'] = "user details updated"
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors':serializer.errors, 'detail':"fields not updated"}, status=status.HTTP_304_NOT_MODIFIED)
    
    # if request.method == 'GET':
    #     pk = int(kwargs['pk'])
    #     try:
    #         user = User.objects.get(pk = int(pk))
    #     except:
    #         return Response(data={'error':f'There is no room with id:{pk}'},status=status.HTTP_404_NOT_FOUND)

    #     serializer = UserSerializer(data = user, many=False)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = UserSerializer