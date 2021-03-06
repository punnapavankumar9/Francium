from django.urls import path, include
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Francium API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   # path('', views.getRoutes),
   path('rooms/', views.RoomListView.as_view()),
   path('rooms/<str:pk>/', views.GetRoomView.as_view()),
   path('create_room/', views.CreateRoomView.as_view()),
   path('room_msgs/<str:pk>/', views.GetMessagesByRoom.as_view()),
   path('send_message/<str:pk>/', views.CreateMessage.as_view()),
   path('room_request/', views.CreateRoomRequest.as_view()),
   path('room_requests/<str:pk>/', views.RoomRequestsView.as_view()),
   path('manage_room_requests/<str:pk>/', views.ManageRoomRequest),
   path('topics/', views.TopicView.as_view()),

   path('accounts/', include('api.accounts.urls')),
]