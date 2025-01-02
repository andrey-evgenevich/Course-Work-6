from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "password1": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Пароль"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Повторите пароль"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email


class AuthForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is None:
            raise forms.ValidationError("Неверный email или пароль")
        self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
