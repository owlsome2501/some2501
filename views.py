from django.shortcuts import render, get_object_or_404
from .models import article, author


def index(request):
    articles = article.objects.all()
    return render(request, "blog/index.html", {"latest_article_list": articles})


def author_index(request):
    authors = author.objects.all()
    return render(request, "blog/author_index.html", {"author_list": authors})


def author_detail(request, author_name):
    au = get_object_or_404(author, name=author_name)
    articles = article.objects.filter(author=au)
    name = au.nickname if au.nickname is not None else au.name
    contex = {
        "name": name,
        "info_list": [{"caption": "Contact me", "detail": au.mail}],
        "description": au.description.content,
        "articles": articles,
    }
    return render(request, "blog/author.html", contex)


def article_detail(request, author_name, file_name):
    art_file_name = file_name + ".md"
    ac = get_object_or_404(article, author__name=author_name, file_name=art_file_name)
    return render(request, "blog/article.html", {"article": ac})
