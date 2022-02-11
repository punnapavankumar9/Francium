from django.urls import path
from . import views
app_name = 'base'

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create_room/', views.create_room, name="create-room"),
    path('update_room/<str:pk>/', views.update_room, name='update-room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete-message'),
    path('topics/', views.topics_view, name="topics"),
    path('activity/', views.activity_view, name="activity"),
    path('room_requests/<str:room_id>/', views.room_requests, name="requests"),
]