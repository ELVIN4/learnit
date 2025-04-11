from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.utils.translation import gettext as _


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label=_("Username"))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    password2 = forms.CharField(
        label=_("Repeat password"), widget=forms.PasswordInput()
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
        labels = {
            "email": "E-Mail",
            "first_name": "First name",
            "last_name": "Last name",
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError(_("Passwords do not match"))

        return cd["password1"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_("E-mail alerady registred"))

        return email
