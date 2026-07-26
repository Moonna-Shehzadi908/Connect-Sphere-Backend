from django.urls import path

from .views import ChangePasswordView, CurrentUserView, LoginView, LogoutView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    #created url for registeration 
    path("register/",RegisterView.as_view(),name="register",),
    #created url for login
    path("login/", LoginView.as_view(), name="login"),
    #created url for token refresh
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    #created url for logout
    path("logout/", LogoutView.as_view(), name="logout"),
    #created url for current user
    path("me/", CurrentUserView.as_view(), name="current-user"),
    #created url for change password
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),
]