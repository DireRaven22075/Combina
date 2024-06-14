# platformReddit/urls.py
from django.urls import path
from .views import RedditApp

urlpatterns = [
    path('connect/', RedditApp.login, name='reddit_connect'),
    path('disconnect/', RedditApp.logout, name='reddit_disconnect'),
    path('post/', RedditApp.create_post, name='reddit_post'),
    path('get-content/', RedditApp.bring_posts, name='reddit_get_content'),
]