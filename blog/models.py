from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=40,
    )
    topik = models.TextField(
        verbose_name="Содержимое статьи",
        max_length=100,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="blog/",
        **NULLABLE,
        help_text="Загрузите фото",
    )
    number_of_views = models.IntegerField(
        verbose_name="количество просмотров",
        default=0,
    )
    date_of_publication = models.DateField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ("title",)

    def __str__(self):
        return f"{self.title}"
