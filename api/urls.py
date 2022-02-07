from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.RoomListView.as_view()),
    path('rooms/<str:pk>/', views.GetRoomView.as_view()),
    path('room_msgs/<str:pk>/', views.GetMessagesByRoom.as_view()),
    path('send_message/<str:pk>/', views.createMessage),
    path('topics/', views.TopicView.as_view()),


    path('accounts/', include('api.accounts.urls')),
]