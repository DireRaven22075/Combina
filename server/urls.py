from django.urls import path
from .views import *
from .sql import *
urlpatterns = [
    path('post', Post, name='post'),
    path('disconnect', Disconnect, name='disconnect')
]