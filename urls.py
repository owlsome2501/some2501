from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:author_name>/', views.author_detail, name='author'),
    path('<str:author_name>/<str:file_name>/',
         views.article_detail,
         name='article')
]
