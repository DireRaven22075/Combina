# platformReddit/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('connect/', RedditView.Connect, name='reddit_connect'),
   
    path('disconnect/', RedditView.Disconnect, name='reddit_disconnect'),
    path('post/', RedditView.CreatePost, name='reddit_post'),
    path('callback/', RedditView.Callback, name='reddit_callback'),
    path('get-content/', RedditView.GetContent, name='reddit_get_content'),

    path('', RedditView.Home, name='reddit_home'),
]