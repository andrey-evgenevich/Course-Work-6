from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "topik",
        "image",
        "number_of_views",
        "date_of_publication",
        "is_published",
    )
    list_filter = ("title", "number_of_views", "date_of_publication")
    search_fields = ("title", "date_of_publication")
