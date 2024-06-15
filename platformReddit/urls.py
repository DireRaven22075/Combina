# platformReddit/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('connect/', RedditView.Connect, name='reddit_connect'),
    path('connectCall/', RedditView.ConnectCall, name='reddit_connectCall'),
    path('disconnect/', RedditView.Disconnect, name='reddit_disconnect'),
    path('post/', RedditView.Post, name='reddit_post'),
    path('callback/', RedditView.Callback, name='reddit_callback'),
    path('get-content/', RedditView.GetContent, name='reddit_get_content'),
]