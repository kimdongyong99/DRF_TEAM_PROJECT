from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from . import views

urlpatterns = [
    
    path("signin/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("signup/", views.UserCreate.as_view()),
    path("logout/", TokenBlacklistView.as_view()),
    path("profile/<str:username>/",views.UserProfileView.as_view()),
    
]
