from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.RoomListView.as_view()),
    path('rooms/<str:pk>/', views.GetRoomView.as_view()),
    path('accounts/', include('api.accounts.urls')),

]