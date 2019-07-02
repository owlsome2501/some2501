import os
from datetime import datetime
import logging
from django.conf import settings
from blog.models import artical_cache
from django.core.management.base import BaseCommand

logger = logging.getLogger('django')


class Command(BaseCommand):
    def build(self):
        logger.info('start build')
        for art_name in os.listdir(settings.ARTICAL_ROOT):
            art_path = os.path.join(settings.ARTICAL_ROOT, art_name)
            logger.debug(f'"{art_path}" process')
            if (not os.path.isfile(art_path) or not art_name.endswith('.md')):
                continue
            try:
                art_cache = artical_cache.objects.get(file_name=art_name)
                if art_cache.is_expired():
                    art_cache.update()
                    logger.info(f'"{art_name}" updated')
            except artical_cache.DoesNotExist:
                artical = artical_cache.parse_md(art_path)
                pub_time = datetime.fromtimestamp(os.path.getmtime(art_path))
                art_cache = artical_cache(file_name=art_name,
                                          title=artical['title'],
                                          pub_time=pub_time,
                                          update_time=pub_time,
                                          content=artical['content'])
                logger.debug(artical['content'])
                logger.info(f'"{art_name}" created')
                art_cache.save()

    def handle(self, *args, **options):
        self.build()
