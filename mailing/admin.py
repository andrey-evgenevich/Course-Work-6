from django.contrib import admin

from mailing.models import Attempt, Client, Mailing, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "frequency",
        "date_time",
    )
    list_filter = ("status",)
    search_fields = ("status",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "topic",
        "owner",
    )
    list_filter = ("id",)
    search_fields = ("topic",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "owner",
    )
    list_filter = ("email", "full_name")
    search_fields = ("email",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "date_time", "status", "mailing")
    list_filter = ("date_time", "status", "mailing")
    search_fields = ("status",)
