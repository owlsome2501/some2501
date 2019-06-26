import os
import markdown
from datetime import datetime, timedelta
import logging
from django.db import models
from django.conf import settings
from django.utils import timezone

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

    @classmethod
    def build(cls):
        logger.info('start build')
        last = cls.last_build_time
        now = timezone.now()
        if last is None or last < now - timedelta(seconds=600):
            cls.last_build_time = now
            for art_name in os.listdir(settings.ARTICAL_ROOT):
                art_path = os.path.join(settings.ARTICAL_ROOT, art_name)
                logger.debug(f'"{art_path}" process')
                if (not os.path.isfile(art_path)
                        and not art_name.endwith('.md')):
                    continue
                try:
                    art_cache = cls.objects.get(file_name=art_name)
                    if art_cache.is_expired():
                        art_cache.update()
                        logger.info(f'"{art_name}" updated')
                except cls.DoesNotExist:
                    artical = artical_cache.parse_md(art_path)
                    pub_time = datetime.fromtimestamp(
                        os.path.getmtime(art_path))
                    art_cache = cls(file_name=art_name,
                                    title=artical['title'],
                                    pub_time=pub_time,
                                    update_time=pub_time,
                                    content=artical['content'])
                    logger.debug(artical['content'])
                    logger.info(f'"{art_name}" created')
                    art_cache.save()
