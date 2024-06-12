from django.urls import path
from .views import *

urlpatterns = [
    path('disconnect/', YoutubeView.Disconnect, name='Disconnect'),
    path('connect/', YoutubeView.Disconnect, name='Disconnect'),
    path('post/', YoutubeView.Disconnect, name='Disconnect'),
    path('get-content/', YoutubeView.Disconnect, name='Disconnect'),
]