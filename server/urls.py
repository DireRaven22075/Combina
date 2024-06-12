from django.urls import path
from .views import *
from .sql import *
urlpatterns = [
    path('post/', ServerView.Post),
    path('test/', ServerView.Test, name='test'),
    path('clear-content/', ServerView.ClearContent, name='clear_content'),
]