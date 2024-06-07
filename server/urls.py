from django.urls import path
from .views import *
from .sql import *
urlpatterns = [
    path('clear-content/', ServerView.ClearContent, name='clear_content'),
]