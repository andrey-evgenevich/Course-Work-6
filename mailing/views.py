from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Blog
from mailing.form import ClientForm, MailingForm
from mailing.models import Client, Mailing
from mailing.services import get_mailing_from_cache


def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(is_active=True).count()
    unique_clients = Client.objects.values("email").distinct().count()
    random_articles = Blog.objects.order_by("?")[:3]

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
        "random_articles": random_articles,
    }
    return render(request, "mailing/index.html", context)


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        return get_mailing_from_cache()


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"  # Укажите ваш шаблон
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем текущего пользователя в форму
        return kwargs

    def form_valid(self, form):
        form.instance.user = (
            self.request.user
        )  # Устанавливаем пользователя для рассылки
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    fields = ("date_time", "frequency", "status", "clients", "message")
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = (
        "mailing.can_block_user",
        "mailing.can_disable_mailing",
        "mailing.can_view_mailing",
    )

    def get_object(self, queryset=None):
        mailing = get_object_or_404(Mailing, id=self.kwargs["pk"])
        print(mailing.owner, self.request.user)
        if mailing.owner != self.request.user:
            raise PermissionDenied("У вас нет прав редактировать рассылку")
        return mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = "mailing.delete_mailing"


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(onwer=user)


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"  # Укажите ваш шаблон
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        # Если вы не хотите устанавливать пользователя, просто уберите эту строку
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailing:client_list")

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if self.request.user == client.owner:
            return HttpResponseForbidden("У вас нет прав для этого списка клиентов")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        clients = get_object_or_404(Client, id=self.kwargs["pk"])
        return clients


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_delete.html"
    success_url = reverse_lazy("mailing:client_list")
    permission_required = "mailing.delete_client"

    def dispatch(self, request, *args, **kwargs):
        client = self.get_object()
        if self.request.user == client.owner:
            return HttpResponseForbidden("У вас нет прав для этого списка клиентов")
        return super().dispatch(request, *args, **kwargs)
