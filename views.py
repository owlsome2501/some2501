from django.shortcuts import render, get_object_or_404
from .models import artical


def index(request):
    articals = artical.objects.all()[-5:]
    return render(request, 'blog/index.html', {'latest_art_list': articals})


def author_detail(request, author_name):
    pass


def artical_detail(request, author_name, file_name):
    art_file_name = file_name + '.md'
    ac = get_object_or_404(artical,
                           author__name=author_name,
                           file_name=art_file_name)
    return render(request, 'blog/artical.html', {'artical': ac})
