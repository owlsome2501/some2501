from django.shortcuts import render
from django.views import generic
from .models import artical_cache


class index(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_artical_list'

    def get_queryset(self):
        artical_cache.build()
        return artical_cache.objects.all()
