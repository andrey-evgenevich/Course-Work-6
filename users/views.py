import secrets


from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, resolve_url
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import AuthForm, UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    template_name = "users/castomuser_form.html"

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_verification/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("mailing:index")
    form_class = AuthForm

    def form_valid(self, form):
        user = form.user_cache
        login(self.request, user)
        return super().form_valid(form)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url("/")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("mailing:index")


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None  # Удаляем токен после подтверждения
    user.save()
    return redirect(reverse("users:login"))
