from .models import article
from haystack import indexes


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
