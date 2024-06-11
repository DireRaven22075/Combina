from django.urls import path
from .views import *

urlpatterns = [
    path('', PageView.Welcome, name="Start"),
    path('home/', PageView.Home, name="Home"),
    path('contacts/', PageView.Contacts, name="Contacts"),
    path('create/', PageView.Create, name="Create"),
    path('accounts/', PageView.Accounts, name='Accounts'),
    path('settings/', PageView.Settings, name='Settings'),
]