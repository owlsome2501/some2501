from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("author", views.author_index, name="author_index"),
    path("author/<str:author_name>/", views.author_detail, name="author"),
    path(
        "article/<str:author_name>/<str:file_name>/",
        views.article_detail,
        name="article",
    ),
    path("search/", include('haystack.urls')),
]
