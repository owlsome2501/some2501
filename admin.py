from django.contrib import admin
from .models import article, author, md_cache, tag

admin.site.register(article)
admin.site.register(author)
admin.site.register(md_cache)
admin.site.register(tag)
