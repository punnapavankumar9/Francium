from typing import OrderedDict
from urllib import request
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from base.models import Message, Room, Topic
from rest_framework.views import APIView
from .serializers import MessageSerializer, RoomSerializer, TopicSerializer
from rest_framework import generics
from .pagination_classes import StandardResultsSetPagination, LargeResultSetPaginator, TestingResultsSetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError

from api import pagination_classes

User = get_user_model()

@api_view(['GET'])
def getRoutes(requests):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
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
    permission_classes = [IsAuthenticated, ]
    queryset = Room.objects.all()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.POST)
        if(serializer.is_valid()):
            print("pavan")
            return Response({'asd':"asdad"})
        else:
            return Response(serializer.errors)


        return None


class GetMessagesByRoom(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = MessageSerializer


    def get_queryset(self):
        pk = self.kwargs.get("pk")
        room = get_object_or_404(Room, id=pk)
        if(room):
            has_permission = room.is_private == False or room.participants.filter(id=self.request.user.id)
            if(has_permission):
                return room.message_set.all()
            else:
                return []
        else:
            return []

    def get(self, request, *args, **kwargs):
        data=self.get_serializer(self.get_queryset(),many=True).data
        if data == []:
            context = {
                "error" : "You don't have permission to view this room messages.",
                }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def createMessage(request, pk):
    if(request.method == "POST"):
        data = {}
        room = get_object_or_404(Room, id=pk)
        if(room.is_private):
            if(not room.participants.filter(id=request.user.id).exists()):
                return Response({'error':'you don\'t have access to this room please request for access'})
        serializer = MessageSerializer(data=request.data)
        if(serializer.is_valid()):
            if("message_image" in  serializer.validated_data):
                isImage = True
                body = serializer.validated_data["message_image"]
            else:
                isImage = False
                body = serializer.validated_data['body']

            serializer.save(
                user = request.user,
                room = room,
                isImage = isImage,
                body = body)
            room.participants.add(request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data=data, status = status.HTTP_406_NOT_ACCEPTABLE)

class TopicView(APIView, StandardResultsSetPagination):

    def get(self,request, *args, **kwargs):
        topics = Topic.objects.all().order_by("name")
        topics = self.paginate_queryset(topics, request)
        serializer = TopicSerializer(topics, many=True)
        response = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', serializer.data)
        ])
        return Response(response, status = status.HTTP_200_OK)
    
    def post(self, request, *args, ** kwargs):
        if not request.user.is_authenticated:
            return Response({"error":"Authentication details not provided"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TopicSerializer(data=request.POST)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

# class GetRoomView(APIView):

#     @authentication_classes([TokenAuthentication, ])
#     @permission_classes([IsAuthenticated,])
#     def get(self, request, pk,  *args, **kwargs):
#         try:
#             room = Room.objects.get(id=int(pk))
#         except:
#             return Response(data={'error':f'There is no room with id:{pk}'},status=status.HTTP_404_NOT_FOUND)
        
#         serializer = RoomSerializer(room, many=False)
#         return Response(serializer.data, status=status.HTTP_200_OK)





# @api_view(['GET'])
# def getRooms(request):
#     rooms = Room.objects.all()
#     serializer = RoomSerializer(rooms, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getRoom(request, pk):
#     room = Room.objects.get(id = pk)
#     serializer = RoomSerializer(room, many= False)
#     return Response(serializer.data)