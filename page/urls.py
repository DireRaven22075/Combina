from django.urls import path
from .views import *
from .sql import *
urlpatterns = [
    path('', Welcome, name='home'),
    path('home/', Home, name='home'),
    path('find/', Find, name='find'),
    path('post/', Post, name='post'),
    path('menu/', Menu, name='menu')
]