from django.shortcuts import render, redirect
from django.http import HttpResponse
import praw
from urllib.parse import urlencode
import requests
from page.models import AccountDB
from .content import Content
from .config import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from django.http import JsonResponse



class RedditView:
    reddit = None
 
    def Disconnect(request):
        account = AccountDB.objects.filter(platform='Reddit').first()
        account.token = ''
        account.connected = False
        account.save()
        if (request.POST.get('page') == 'welcome2'):
            return redirect('/start')
        else:
            return redirect('/accounts')

    def Connect(request):
        auth_url = 'https://www.reddit.com/api/v1/authorize'
        params = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'state': 'random_string',  # Should be a random string
            'redirect_uri': 'http://localhost:8000/Reddit/callback/',
            'duration': 'permanent',
            'scope': 'identity read submit mysubreddits'
        }
        auth_url_full = f'{auth_url}?{urlencode(params)}'

        return render(request, 'reddit/login.html', {'auth_url': auth_url_full})
    
    def Callback(request):
        code = request.GET.get('code')
        if not code:
            return redirect('/Reddit/connect')
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        post_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:8000/Reddit/callback/',
        }
        headers = {
            'User-Agent': USER_AGENT
        }
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                                auth=auth, data=post_data, headers=headers)
        
        response_info = response.json()
        refresh_token = response_info.get('refresh_token')
        print("code is ", code)
        print("type is ", type(code))
        print("response_info", response_info)
        print("token", refresh_token)
        # PRAW 초기화
        RedditView.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            refresh_token=refresh_token
        )
    
        try:
            user = RedditView.reddit.user.me()
            print(user.name) 
            account = AccountDB.objects.filter(platform='Reddit').first()
            account.token = code
            account.name = user.name
            account.connected = True
            account.icon = user.icon_img
            account.save()
        except Exception as e:
            print(f'Failed to get user: {e}')
            RedditView.reddit = None
            return redirect('/Reddit/connect')
        
        return redirect('/Reddit/connect?code=' + code)

  
    def GetContent(request):
        reddit = RedditView.reddit
        if reddit:
            success = Content(reddit)
            if success:
                return JsonResponse({'message': 'success get Content'})
            
            
            return JsonResponse({'error': 'Failed to get Content'}, status=400)
        return redirect('/Reddit/connect')
    
    def Post(request):
        return HttpResponse('Post')
    # Compare this snippet from platformReddit/views.py:


    def get_reddit_instance():
        return RedditView.reddit

