from django.urls import path
from .views import YouTubeView

urlpatterns = [
    path('', YouTubeView.home, name='home'),
    path('login/', YouTubeView.Connect, name='login'),
    path('callback/', YouTubeView.ConnectCallback, name='callback'),
    path('logout/', YouTubeView.Disconnect, name='logout'),
    path('search_videos/', YouTubeView.GetContent, name='search_videos'),
    path('recommended/', YouTubeView.GetContent, name='recommended'),
]
