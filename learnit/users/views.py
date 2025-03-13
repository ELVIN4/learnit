from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from .forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy("main")
