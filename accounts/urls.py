from django.urls import path, reverse_lazy
from . import views

app_name = "accounts"

urlpatterns = [

    path('login/', views.login_view, name="login"),
    path('login/<str:from_password_reset>/', views.login_view2, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('update_user/', views.update_user_view, name="update-user"),
    path('profile/<str:pk>/', views.profile_view, name="profile"),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/',views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

]