from django.urls import path
from .views import YouTubeView

urlpatterns = [
    path('connect/', YouTubeView.Connect, name='login'),
    path('callback/', YouTubeView.ConnectCallback, name='callback'),
    path('disconnect/', YouTubeView.Disconnect, name='logout'),
    path('get-content/', YouTubeView.GetContent, name='recommended'),
    path('clear-contents/', YouTubeView.ClearContent, name='clear_contents'),  # Add this line
]
