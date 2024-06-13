from django.urls import path
from .views import RedditView

urlpatterns = [
    path('connect/', RedditView.Connect, name='reddit_connect'),
    path('connect/callback/', RedditView.ConnectCallback, name='reddit_connect_callback'),
    path('disconnect/', RedditView.Disconnect, name='reddit_disconnect'),
    path('post/', RedditView.Post, name='reddit_post'),
    path('content/', RedditView.GetContent, name='reddit_get_content'),
]
