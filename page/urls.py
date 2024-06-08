from django.urls import path
from .views import *

urlpatterns = [
    path('', PageView.Init, name="Start"),
    path('test/', PageView.Test, name="Test"),
    path('home/', PageView.Home, name="Home"),
    path('explore/', PageView.Explore, name="Search"),
    path('contacts/', PageView.Contacts, name="Contacts"),
    path('watch/', PageView.Watch, name="Video"),
    path('create/', PageView.Create, name="Create"),
    path('accounts/', PageView.Accounts, name='Accounts'),
    path('settings/', PageView.Settings, name='Settings'),
]