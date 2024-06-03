from django.urls import path
from .views import *

urlpatterns = [
    path('', PageView.Welcome, name='welcome'),
    path('home/', PageView.Home, name='home'),
    path('post/', PageView.Post, name='post'),
    path('menu/', PageView.Menu, name='menu')
]