from django.urls import path
from .views import *

urlpatterns = [
    path('', PageView.Init, name="Start"),
    path('home/', PageView.Home, name="Home"),
    path('search/', PageView.Search, name="Search"),
    path('video/', PageView.Video, name="Video"),
    path('create/', PageView.Create, name="Create"),
    path('contacts/', PageView.Contacts, name="Contacts")
]