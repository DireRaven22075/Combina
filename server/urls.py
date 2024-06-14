from django.urls import path
from .views import *
urlpatterns = [
    path('disconnect/', ServerView.Disconnect),
    path('post/', ServerView.Post),
    path('get-content/', ServerView.GetContent),
    path('clear-content/', ServerView.ClearContent),
]