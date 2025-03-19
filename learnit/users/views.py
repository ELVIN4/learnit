from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:signin")
