from . import views
from django.urls import include, path
from .views import *

urlpatterns = [
    path('home/', views.home, name="home"),
    path('search/', views.search, name="search_posts"),
]