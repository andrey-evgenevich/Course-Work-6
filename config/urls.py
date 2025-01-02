from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mailing.urls", namespace="mailing")),
    path("users/", include("users.urls", namespace="users")),
    path("blog/", include("blog.urls", namespace="blog")),
]
