from django.contrib import admin
from .models import artical, author, md_cache

admin.site.register(artical)
admin.site.register(author)
admin.site.register(md_cache)
