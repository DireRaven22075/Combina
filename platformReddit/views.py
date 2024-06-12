from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from page.models import *
from .auth import get_credentials
from .posts import get_saved_posts, get_upvoted_posts, get_subreddit_posts, get_random_subscribed_posts
# Create your views here.
class RedditView:
    # Connect to Reddit
    def Connect(reuqest):
        return render(reuqest, 'Reddit/connect.html')
    
    def ConnectCallback(request):
        return render(request, 'Reddit/connect.html')
    
    # Disconnect from Reddit
    def Disconnect(request):
        user = AccountDB.objects.filter(platform="Reddit").first()
        user.name = None
        user.token = None
        user.connected = False
        user.icon = None
        user.tag = None
        user.save()
        return redirect(request.META.get('HTTP_REFERER', '/home'))
    
    # Post content to Reddit
    def Post(request):
        return JsonResponse({"status": "success"})
    
    # Get content from Reddit
    def GetContent(request):
        return JsonResponse({"status": "success"})