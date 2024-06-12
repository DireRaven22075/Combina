from django.urls import path
from .views import RedditView

urlpatterns = [
    path('connect/', RedditView.Connect),
    path('disconnect/', RedditView.Connect),
    path('post/', RedditView.Post),
    path('get-content/', RedditView.GetContent),
]