from django.shortcuts import render, get_object_or_404
from .models import artical_cache


def index(request):
    acs = artical_cache.objects.all()
    return render(request, 'blog/index.html', {'latest_artical_list': acs})


def author(request, author):
    pass


def artical(request, author, file_name):
    artical_file_name = file_name + '.md'
    ac = get_object_or_404(artical_cache,
                           author__name=author,
                           file_name=artical_file_name)
    return render(request, 'blog/artical.html', {'artical_cache': ac})
