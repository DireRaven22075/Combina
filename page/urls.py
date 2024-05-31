from django.urls import path
from .views import *
from .sql import *
from asgiref.sync import async_to_sync
urlpatterns = [
    path('', Home, name='home'),
    path('home/', Home, name='home'),
    path('find/', Find, name='find'),
    path('post/', Post, name='post'),
    path('chat/', Chat, name='chat'),
    path('chat/<str:platform>/<int:id>/', InChat, name='inchat'),
    path('menu/', Menu, name='menu'),
    path('server/post', Server.Post),
    path('server/disconnect', Disconnect, name='disconnect'),
    path('temp/test', DBTest, name='temp'),
]