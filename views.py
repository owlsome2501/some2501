from django.shortcuts import render, get_object_or_404
from .models import artical, author


def index(request):
    articals = artical.objects.all()
    return render(request, 'blog/index.html',
                  {'latest_artical_list': articals})


def author_detail(request, author_name):
    au = get_object_or_404(author, name=author_name)
    articals = artical.objects.filter(author=au)
    name = au.nickname if au.nickname is not None else au.name
    contex = {
        'name': name,
        'info_list': [{
            'caption': 'Contact me',
            'detail': au.mail
        }],
        'description': au.description.content,
        'articals': articals
    }
    return render(request, 'blog/author.html', contex)


def artical_detail(request, author_name, file_name):
    art_file_name = file_name + '.md'
    ac = get_object_or_404(artical,
                           author__name=author_name,
                           file_name=art_file_name)
    return render(request, 'blog/artical.html', {'artical': ac})
