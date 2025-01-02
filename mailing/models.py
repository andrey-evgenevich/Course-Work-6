from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Client(models.Model):
    email = models.EmailField(verbose_name="электронная почта", unique=False)
    full_name = models.CharField(verbose_name="ФИО", max_length=100)
    comment = models.TextField(
        verbose_name="комментарий",
        max_length=100,
        **NULLABLE,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", "full_name"]

    def __str__(self):
        return self.email


class Message(models.Model):
    topic = models.CharField(verbose_name="тема письма", max_length=30)
    body = models.TextField(verbose_name="тело письма", max_length=100)
    owner = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "topic",
        ]

    def __str__(self):
        return self.topic


class Mailing(models.Model):
    CHOICES_TIME = (
        ("Day", "Раз в день"),
        ("Week", "Раз в неделю"),
        ("Month", "Раз в месяц"),
    )
    CHOICES_STATUS = (
        ("created", "создана"),
        ("running", "запущена"),
        ("completed", "завершена"),
    )

    date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата и время первой отправки рассылки",
        help_text="Выберите время отправки",
        **NULLABLE,
    )
    frequency = models.CharField(
        verbose_name="Периодичность",
        max_length=20,
        choices=CHOICES_TIME,
        help_text="Выберите периодичность отправки",
        **NULLABLE,
    )
    status = models.CharField(
        verbose_name="Статус рассылки",
        max_length=20,
        choices=CHOICES_STATUS,
        default="created",
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name="Клиенты",
        help_text="выберите клиентов для рассылки",
        related_name="clients",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name="Сообщение",
        help_text="Выберите сообщение",
        related_name="messages",
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["date_time", "status"]
        permissions = [
            ("can_view_mailing", "Can view mailing"),
            ("can_block_user", "Can block user"),
            ("can_disable_mailing", "Can disable mailing"),
        ]

    def __str__(self):
        return self.status


class Attempt(models.Model):
    date_time = models.DateTimeField(
        verbose_name="дата и время последней попытки", auto_now=True
    )
    status = models.BooleanField(
        verbose_name="статус попытки",
    )
    server_response = models.TextField(
        verbose_name="ответ почтового сервера",
        **NULLABLE,
    )
    mailing = models.ForeignKey(
        Mailing,
        verbose_name="рассылка",
        on_delete=models.CASCADE,
        related_name="Mailings",
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["date_time", "status"]

    def __str__(self):
        # Возвращаем строку, описывающую статус
        return "Успех" if self.status else "Неудача"
    