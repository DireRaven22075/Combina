from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('home/', Home, name='home'),
    path('find/', Find, name='find'),
    path('post/', Post, name='post'),
    path('chat/', Chat, name='chat'),
    path('chat/<str:platform>/<int:id>/', InChat, name='inchat'),
    path('menu/', Menu, name='menu'),
]