from django.urls import path
from . import views
app_name = "accounts"

urlpatterns = [

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('update_user/', views.update_user_view, name="update-user"),
    path('profile/<str:pk>/', views.profile_view, name="profile"),



]