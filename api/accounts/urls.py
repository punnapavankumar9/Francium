from django.urls import path
from . import views

urlpatterns = [
    path('login/',  views.CustomAuthToken.as_view()),
    path('register/',  views.registerUserView),
    path('update/', views.userDetailsView),
    path('user/<str:pk>/', views.UserDetailsView.as_view()),
    
]