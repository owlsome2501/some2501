from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:author>/', views.author, name='author'),
    path('<str:author>/<str:file_name>/', views.artical, name='artical')
]
