from django.urls import path
from . import views
app_name = 'base'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create_room/', views.create_room, name="create-room"),
    path('update_room/<str:pk>/', views.update_room, name='update-room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete-room'),

]