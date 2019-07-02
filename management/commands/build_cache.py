from os import listdir, path
from datetime import datetime
import logging
from django.conf import settings
from blog.models import artical_cache, author, parse_md
from django.core.management.base import BaseCommand

logger = logging.getLogger('django')


class Command(BaseCommand):
    def build_author(self):
        for author_name in listdir(settings.ARTICAL_ROOT):
            author_home = path.join(settings.ARTICAL_ROOT, author_name)
            author_self = path.join(author_home, author_name + 'md')
            logger.debug(f'"{author_home}" process')
            if path.isfile(author_self):
                meta, description = parse_md(author_self)
                nickname = meta.get('nickname', (author_name, ))[0]
                mail = meta.get('mail', (None, ))[0]
                new_author = author(name=author_name,
                                    nickname=nickname,
                                    mail=mail,
                                    description=description)
                logger.debug(description)
                logger.info(f'"{author_name}" created')
                new_author.save()

    def build_artical(self):
        logger.info('start build')
        for author_name in listdir(settings.ARTICAL_ROOT):
            author_home = path.join(settings.ARTICAL_ROOT, author_name)
            for art_name in listdir(author_home):
                art_path = path.join(author_home, art_name)
                logger.debug(f'"{art_path}" process')
                if (not path.isfile(art_path) or not art_name.endswith('.md')):
                    continue
                try:
                    art_cache = artical_cache.objects.get(file_name=art_name)
                    if art_cache.is_expired():
                        art_cache.update()
                        logger.info(f'"{art_name}" updated')
                except artical_cache.DoesNotExist:
                    artical = parse_md(art_path)
                    pub_time = datetime.fromtimestamp(path.getmtime(art_path))
                    art_cache = artical_cache(file_name=art_name,
                                              title=artical['title'],
                                              pub_time=pub_time,
                                              update_time=pub_time,
                                              content=artical['content'])
                    logger.debug(artical['content'])
                    logger.info(f'"{art_name}" created')
                    art_cache.save()

    def handle(self, *args, **options):
        self.build_author()
        self.build_artical()
