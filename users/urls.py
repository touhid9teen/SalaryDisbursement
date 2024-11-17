from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, LoginView, UserInfoView, RefreshTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserInfoView.as_view(), name='user_info'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
]