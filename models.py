import os
import markdown
from datetime import datetime, timezone
import logging
from django.db import models
from django.conf import settings

logger = logging.getLogger('django')


class md_cache(models.Model):
    content = models.TextField()
    update_time = models.DateTimeField()
    file_path = models.CharField(max_length=512)

    def is_expired(self):
        p = os.path.join(settings.ARTICAL_ROOT, self.file_path)
        return md_cache.get_mtime(p) > self.update_time

    def update(self):
        p = os.path.join(settings.ARTICAL_ROOT, self.file_path)
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
        p = os.path.join(settings.ARTICAL_ROOT, file_path)
        meta, content = md_cache.parse_md(p)
        update_time = md_cache.get_mtime(p)
        ins = md_cache(content=content,
                       file_path=file_path,
                       update_time=update_time)
        return meta, ins


class author(models.Model):
    name = models.CharField(max_length=30)
    mail = models.EmailField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, black=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def is_expired(self):
        return self.description.is_expired()

    def update(self):
        meta = self.description.update()
        self.mail = meta.get('mail', (None, ))[0]
        self.nickname = meta.get('nickname', (None, ))[0]
        self.save()

    @staticmethod
    def mk_author(name: str):
        author_home = os.path.join(settings.ARTICAL_ROOT, name)
        author_self = os.path.join(author_home, name + '.md')
        if not os.path.isfile(author_self):
            return None
        logger.debug(f'"{author_home}" process')
        meta, description = md_cache.mk_md_cache(author_self)
        mail = meta.get('mail', (None, ))[0]
        nickname = meta.get('nickname', (None, ))[0]
        return author(name=name,
                      mail=mail,
                      nickname=nickname,
                      description=description)


class artical(models.Model):
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    pub_time = models.DateTimeField()
    content = models.ForeignKey(md_cache, on_delete=models.CASCADE)
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

    @staticmethod
    def mk_artical(author: author, file_name: str):
        file_path = os.path.join(author.name, file_name)
        meta, content = md_cache.mk_md_cache(file_path)
        title = meta.get('title', ('████████████████████', ))[0]
        pub_time = meta.get('time', (content.update_time, ))[0]
        return artical(file_name=file_name,
                       title=title,
                       pub_time=pub_time,
                       content=content,
                       author=author)
