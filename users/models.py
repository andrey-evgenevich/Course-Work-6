from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    USERNAME_FIELD = "email"
    token = models.CharField(max_length=32, **NULLABLE)
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Уникальное имя для обратного доступа
        blank=True,
        help_text="Группы, к которым принадлежит этот пользователь. Пользователь получит все разрешения, "
        "предоставленные каждой из своих групп.",
        related_query_name="custom_user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Уникальное имя для обратного доступа
        blank=True,
        help_text="Конкретные разрешения для этого пользователя.",
        related_query_name="custom_user_permission",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
    