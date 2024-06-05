from django.urls import path
from .views import *

urlpatterns = [
    path('test/', PageView.Test, name="Test"),
    path('', PageView.Init, name="Start"),
    path('home/', PageView.Home, name="Home"),
    path('explore/', PageView.Explore, name="Search"),
    path('contacts/', PageView.Contacts, name="Contacts"),
    path('watch/', PageView.Watch, name="Video"),
    path('create/', PageView.Create, name="Create"),
]