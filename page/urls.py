from django.urls import path
from .views import *
from .sql import *
from asgiref.sync import async_to_sync
urlpatterns = [
    path('', Welcome, name='home'),
    path('home/', Home, name='home'),
    path('find/', Find, name='find'),
    path('post/', Post, name='post'),
    path('menu/', Menu, name='menu'),
]