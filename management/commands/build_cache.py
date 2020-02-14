from os import listdir, path
import logging
from django.conf import settings
from blog.models import article, author, tag
from django.core.management.base import BaseCommand

logger = logging.getLogger("django")


class Command(BaseCommand):
    def gc(self):
        logger.info("start clean")
        for au in author.objects.all():
            au.gc()
        for art in article.objects.all():
            art.gc()
        # tag gc must after article
        for t in tag.objects.all():
            t.gc()

    def build(self):
        logger.info("start build")
        for author_name in listdir(settings.ARTICLE_ROOT):
            try:
                logger.debug(f'"{author_name}" process')
                au = author.objects.get(name=author_name)
                if au.is_expired():
                    au.update()
                    logger.info(f'"{au.name}" updated')
            except author.DoesNotExist:
                au = author.mk_author(author_name)
                if au is not None:
                    logger.info(f'"{au.name}" created')
                else:
                    continue
            author_home = path.join(settings.ARTICLE_ROOT, author_name)
            for art_name in listdir(author_home):
                art_path = path.join(author_home, art_name)
                logger.debug(f'"{art_path}" process')
                if not path.isfile(art_path) or not art_name.endswith(".md"):
                    continue
                try:
                    art = article.objects.get(author=au, file_name=art_name)
                    if art.is_expired():
                        art.update()
                        logger.info(f'"{art_name}" updated')
                except article.DoesNotExist:
                    art = article.mk_article(au, art_name)
                    if art is not None:
                        logger.info(f'"{art_name}" created')

    def handle(self, *args, **options):
        self.gc()
        self.build()
