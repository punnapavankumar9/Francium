from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegisterUserSerializer, SetNewPasswordSerializer, UserSerializer, PasswordUpdateSerializer, PasswordResetSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_yasg.utils import swagger_auto_schema


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

@swagger_auto_schema(method='post', request_body=RegisterUserSerializer)
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

    
@swagger_auto_schema(method='put', request_body=UserSerializer)
@api_view(['PUT',])
@permission_classes([IsAuthenticated, ])
def UserUpdateView(request, *args, **kwargs):
    if request.method == 'PUT':
        print(request.user)
        serializer = UserSerializer(request.user ,data = request.data, partial=True)
        if(serializer.is_valid()):
            user = serializer.save()
            data = {}
            data['message'] = "user details updated"
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'errors':serializer.errors, 'detail':"fields not updated"}, status=status.HTTP_304_NOT_MODIFIED)

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = "pk"
    serializer_class = UserSerializer

class UserPasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            user = serializer.save()
            if(hasattr(user, 'auth_token')):
                user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail':"A mail with password reset instructions has been sent to your email address."}, status=status.HTTP_200_OK)


@api_view(['GET',])
def PasswordTokenCheckView(self, request, uidb64, token, **kwargs):
    if request.method == 'POST':
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)
        except:
            return Response({'detail':"please enter a valid url or try to reset the password after sometime"})
        if not PasswordResetTokenGenerator().check_token(user = user, token=token):
            return Response({'detail':"Password reset process failed please generate a new token"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail':"Password reset token verification success", 'token':token, 'uidb64':uidb64}, status=status.HTTP_200_OK)

class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'detail':"password reset successfully completed"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
