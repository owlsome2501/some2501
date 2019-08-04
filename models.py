import os
import markdown
from datetime import datetime, timezone
import logging
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

logger = logging.getLogger('django')


class md_cache(models.Model):
    content = models.TextField()
    update_time = models.DateTimeField()
    file_path = models.CharField(max_length=512)

    def __str__(self):
        return self.file_path

    def is_expired(self):
        p = os.path.join(settings.ARTICLE_ROOT, self.file_path)
        return md_cache.get_mtime(p) > self.update_time

    def update(self):
        p = os.path.join(settings.ARTICLE_ROOT, self.file_path)
        meta, content = md_cache.parse_md(p)
        self.content = content
        self.update_time = md_cache.get_mtime(p)
        self.save()
        return meta

    @staticmethod
    def get_mtime(p):
        return datetime.fromtimestamp(os.path.getmtime(p), timezone.utc)

    @staticmethod
    def parse_md(md_file_path):
        with open(md_file_path) as md_file:
            md_str = md_file.read()

        # use pyhton-markdown
        md_ext = ['extra', 'codehilite', 'meta']
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

    def mk_md_cache(file_path):
        '''
        parse markdown file and creat md_cache
        '''
        # load markdown file with relative path
        p = os.path.join(settings.ARTICLE_ROOT, file_path)
        meta, content = md_cache.parse_md(p)
        update_time = md_cache.get_mtime(p)
        ins = md_cache(content=content,
                       file_path=file_path,
                       update_time=update_time)
        ins.save()
        return meta, ins


class author(models.Model):
    name = models.CharField(max_length=30)
    mail = models.EmailField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    description = models.OneToOneField(md_cache, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_expired(self):
        return self.description.is_expired()

    def update(self):
        meta = self.description.update()
        self.mail = meta.get('mail', (None, ))[0]
        self.nickname = meta.get('nickname', (None, ))[0]
        self.save()

    def gc(self):
        author_home = os.path.join(settings.ARTICLE_ROOT, self.name)
        author_self_full = os.path.join(author_home, self.name + '.md')
        if not os.path.isfile(author_self_full):
            self.delete()

    # def delete(self, *args, **kwargs):
    #     self.description.delete()
    #     super().delete(*args, **kwargs)

    @staticmethod
    def mk_author(name: str):
        author_home = os.path.join(settings.ARTICLE_ROOT, name)
        author_self = os.path.join(name, name + '.md')
        author_self_full = os.path.join(author_home, name + '.md')
        if not os.path.isfile(author_self_full):
            return None
        logger.debug(f'"{name}" process')
        meta, description = md_cache.mk_md_cache(author_self)
        mail = meta.get('mail', (None, ))[0]
        nickname = meta.get('nickname', (None, ))[0]
        au = author(name=name,
                    mail=mail,
                    nickname=nickname,
                    description=description)
        au.save()
        return au


class article(models.Model):
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    pub_time = models.DateTimeField()
    content = models.OneToOneField(md_cache, on_delete=models.CASCADE)
    author = models.ForeignKey(author, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.author}]{self.file_name}'

    def is_expired(self):
        return self.content.is_expired()

    def update(self):
        meta = self.content.update()
        self.title = meta.get('title', ('████████████████████', ))[0]
        self.pub_time = meta.get('time', (self.content.update_time, ))[0]
        self.save()

    def gc(self):
        author_home = os.path.join(settings.ARTICLE_ROOT, self.author.name)
        file_path = os.path.join(author_home, self.file_name)
        if not os.path.isfile(file_path):
            self.delete()

    class Meta:
        ordering = ['-pub_time']

    # use signal instead
    # def delete(self, *args, **kwargs):
    #     self.content.delete()
    #     logger.info(f'"{self.content}" deleted')
    #     super().delete(*args, **kwargs)

    @staticmethod
    def mk_article(author: author, file_name: str):
        if file_name == author.name + '.md':
            return None
        file_path = os.path.join(author.name, file_name)
        meta, content = md_cache.mk_md_cache(file_path)
        title = meta.get('title', ('████████████████████', ))[0]
        pub_time = meta.get('time', (content.update_time, ))[0]
        art = article(file_name=file_name,
                      title=title,
                      pub_time=pub_time,
                      content=content,
                      author=author)
        art.save()
        return art


# https://stackoverflow.com/a/33205503


@receiver(post_delete, sender=author)
def auto_delete_md_cache_with_author(sender, instance, **kwargs):
    instance.description.delete()


@receiver(post_delete, sender=article)
def auto_delete_md_cache_with_article(sender, instance, **kwargs):
    instance.content.delete()
