from django.urls import path
from .views import *
urlpatterns = [
    path("register",Register.as_view(),name="register"),
    path("login",Login.as_view(),name="login"),
    path("refresh",TokenRefreshView.as_view(),name="token-refresh"),
    path("logout",Logout.as_view(),name="logout"),
    path("change-password",ChangePassword.as_view(),name="password-change"),
    path("password-forgot-request",ForgotPasswordRequest.as_view(),name="password-forgot-request")
]