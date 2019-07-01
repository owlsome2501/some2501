import os
import markdown
from datetime import datetime
import logging
from django.db import models
from django.conf import settings

logger = logging.getLogger('django')


class artical_cache(models.Model):
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    pub_time = models.DateTimeField()
    update_time = models.DateTimeField()
    content = models.TextField()

    last_build_time = None

    def __str__(self):
        return self.file_name

    def is_expired(self):
        p = os.path.join(settings.ARTICAL_ROOT, self.file_name)
        return datetime.fromtimestamp(os.path.getmtime(p)) > self.update_time

    def update(self):
        p = os.path.join(settings.ARTICAL_ROOT, self.file_name)
        artical = artical_cache.parse_md(p)
        self.update_time = datetime.fromtimestamp(os.path.getmtime(p))
        self.title = artical['title']
        self.content = artical['content']
        self.save()

    @staticmethod
    def parse_md(md_file_path):
        md_ext = ['extra', 'codehilite', 'meta']
        with open(md_file_path) as md_file:
            md_str = md_file.read()
        md = markdown.Markdown(extensions=md_ext)
        content = md.convert(md_str)
        logger.debug(content)
        title = md.Meta.get('title', ('████████████████████', ))[0]
        logger.debug(title)
        return {'title': title, 'content': content}
