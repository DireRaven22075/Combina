from django.urls import path
from .views import YouTubeView

urlpatterns = [
    path('connect/', YouTubeView.Connect, name='connect'),
    path('callback/', YouTubeView.ConnectCallback, name='callback'),
    path('disconnect/', YouTubeView.Disconnect, name='disconnect'),
    path('get-content/', YouTubeView.GetContent, name='get_content'),
]