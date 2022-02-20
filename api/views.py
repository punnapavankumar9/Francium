from email.policy import HTTP
from multiprocessing import AuthenticationError
from typing import OrderedDict
from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from base.models import Message, Request, Room, Topic
from rest_framework.views import APIView
from .serializers import MessageSerializer, RoomSerializer, TopicSerializer, UserRoomRequestsSerializer
from rest_framework import generics
from .pagination_classes import StandardResultsSetPagination, LargeResultSetPaginator, TestingResultsSetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError
from drf_yasg.utils import swagger_auto_schema,swagger_serializer_method
from drf_yasg import openapi

from api import custom_validators, pagination_classes

User = get_user_model()


@api_view(['GET'])
def getRoutes(requests):
    routes = ['GET /api', 'GET /api/rooms', 'GET /api/rooms/:id']
    return Response(routes)


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all().order_by('-updated')
    pagination_class = StandardResultsSetPagination
    serializer_class = RoomSerializer


class GetRoomView(generics.RetrieveAPIView):
    lookup_field = "pk"
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Room.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            topic, created = Topic.objects.get_or_create(name = request.data.get('topic'))
            room = serializer.save(host=request.user, topic = topic)
            room.participants.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

        return None


class GetMessagesByRoom(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        room = get_object_or_404(Room, id=pk)
        if (room):
            has_permission = room.is_private == False or room.participants.filter(
                id=self.request.user.id)
            if (has_permission):
                return room.message_set.all()
            else:
                raise ValidationError(
                    "You don't have permission to view this room messages.")
        else:
            return []



class CreateMessage(APIView):
    serializer_class = MessageSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @swagger_auto_schema(request_body=MessageSerializer, )
    def post(self, request, pk, *args, **kwargs):
        data = {}
        if not custom_validators.pk_int_validater(pk):
            return Response(
                {'error': 'please provide a valid room_id(int) in url'},
                status=status.HTTP_400_BAD_REQUEST)
        room = get_object_or_404(Room, id=pk)
        if (room.is_private):
            if (not room.participants.filter(id=request.user.id).exists()):
                return Response({
                    'error':
                    'you don\'t have access to this room please request for access'
                })
        serializer = MessageSerializer(data=request.data)
        if (serializer.is_valid()):
            if ("message_image" in serializer.validated_data):
                isImage = True
                body = serializer.validated_data["message_image"]
            else:
                isImage = False
                body = serializer.validated_data['body']

            serializer.save(user=request.user,
                            room=room,
                            isImage=isImage,
                            body=body)
            room.participants.add(request.user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)


class TopicView(APIView, StandardResultsSetPagination):
    serializer_class = TopicSerializer
    query_set = Topic.objects.all()
    


    def get(self, request, *args, **kwargs):
        topics = Topic.objects.all().order_by("name")
        topics = self.paginate_queryset(topics, request)
        serializer = TopicSerializer(topics, many=True)
        response = OrderedDict([('count', self.page.paginator.count),
                                ('next', self.get_next_link()),
                                ('previous', self.get_previous_link()),
                                ('results', serializer.data)])
        return Response(response, status=status.HTTP_200_OK)



    @swagger_auto_schema(request_body=TopicSerializer, )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication details not provided"},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = TopicSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



class RoomRequestsView(generics.ListAPIView, StandardResultsSetPagination):
    serializer_class = UserRoomRequestsSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        room = get_object_or_404(Room, pk=pk)
        if(self.request.user != room.host):
            return Response({'Error':"You don't have access to view this page"})
        return super().list(request, *args, **kwargs)


    def get_queryset(self):
        pk = self.kwargs.get("pk")
        room = get_object_or_404(Room, pk=pk)
        return room.request_set.all()


@swagger_auto_schema(method='post' ,request_body=openapi.Schema(type=openapi.TYPE_OBJECT,   properties={
            'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='Accept/Decline'),
            }))
@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def ManageRoomRequest(request, pk, *args, **kwargs):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=pk)
        join_requests = room.request_set.all()
        for req in join_requests:
            if(request.data.get(req.user.username) == 'Accept'):
                room.participants.add(req.user)
                req.delete()
            elif(request.data.get(req.user.username) == 'Decline'):
                req.delete()
        return Response({'details':"success"})


class CreateRoomRequest(generics.CreateAPIView):
    serializer_class = UserRoomRequestsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            room = get_object_or_404(Room, pk= request.data['room'])
            if not room.request_set.filter(user=request.user).exists() and request.user not in room.participants:
                serializer.save(user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail':'request already sent to room host'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

