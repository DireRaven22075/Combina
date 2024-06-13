from django.urls import path
from .views import *
urlpatterns = [
    path('disconnect/', ServerView.Disconnect),
    path('post/', ServerView.Post),
    path('clear-content/', ServerView.ClearContent, name='clear_content'),
]