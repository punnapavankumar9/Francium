from django.urls import path
from . import views
app_name = 'base'

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('profile/<str:pk>/', views.profile_view, name="profile"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create_room/', views.create_room, name="create-room"),
    path('update_room/<str:pk>/', views.update_room, name='update-room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete-message'),

    path('update_user/', views.update_user_view, name="update-user"),

    path('topics/', views.topics_view, name="topics"),
    path('activity/', views.activity_view, name="activity"),

]