from django.urls import path

from .views import LoginUser, RegisterUser
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path("login/", LoginUser.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", RegisterUser.as_view(), name="signup"),
]
