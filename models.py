import os
import markdown
from datetime import datetime, timezone
import logging
from django.db import models
from django.conf import settings

logger = logging.getLogger('django')


class author(models.Model):
    name = models.CharField(max_length=30)
    mail = models.EmailField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, black=True)
    description = models.TextField()

    def update(self):
        pass


class artical_cache(models.Model):
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    pub_time = models.DateTimeField()
    update_time = models.DateTimeField()
    content = models.TextField()
    author = models.ForeignKey(author, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.author}]{self.file_name}'

    def update(self):
        p = os.path.join(settings.ARTICAL_ROOT, self.author, self.file_name)
        meta, artical = parse_md(p)
        self.update_time = artical_cache.get_mtime(p)
        self.title = meta.get('title', ('████████████████████', ))[0]
        self.content = artical
        self.save()


class md_cache(models.Model):
    content = models.TextField()

    def is_expired(self):
        p = os.path.join(settings.ARTICAL_ROOT, self.file_name)
        return artical_cache.get_mtime(p) > self.update_time

    @staticmethod
    def get_mtime(p):
        return datetime.fromtimestamp(os.path.getmtime(p), timezone.utc)

    @staticmethod
    def parse_md(md_file_path):
        md_ext = ['extra', 'codehilite', 'meta']
        with open(md_file_path) as md_file:
            md_str = md_file.read()
        md = markdown.Markdown(extensions=md_ext)
        content = md.convert(md_str)
        logger.debug(content)
        # example output of md.Meta :
        # {
        #     'title' : ['My Document'],
        #     'summary' : ['A brief description of my document.'],
        #     'authors' : ['Waylan Limberg', 'John Doe'],
        #     'date' : ['October 2, 2007'],
        #     'blank-value' : [''],
        #     'base_url' : ['http://example.com']
        # }
        return md.Meta, content
