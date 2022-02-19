from django.urls import path
from . import views

urlpatterns = [
    path('login/',  views.CustomAuthToken.as_view()),
    path('register/',  views.registerUserView),
    path('update/', views.UserUpdateView),
    path('user/<str:pk>/', views.UserDetailsView.as_view()),
    path('password_change/', views.UserPasswordChangeView.as_view()),
    path('password-reset/', views.RequestPasswordResetEmail.as_view()),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordTokenCheckView, name="password-reset-confirm"),
    path('password_reset_complete/', views.SetNewPassword.as_view(), name="password-reset-complete"),

]