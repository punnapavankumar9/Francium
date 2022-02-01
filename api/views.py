from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from base.models import Room
from .serializers import RoomSerializer
from rest_framework import generics
from rest_framework.views import APIView
from .pagination_classes import StandardResultsSetPagination, LargeResultSetPaginator
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

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

