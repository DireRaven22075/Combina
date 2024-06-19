from django.shortcuts import render, redirect
from django.http import HttpResponse
import praw
from urllib.parse import urlencode
import requests
from page.models import AccountDB, ContentDB, FileDB
from page.views import parameters
from .content import Content
from .config import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from django.http import JsonResponse
from .post import Post
import json
import base64
from django.core.files.base import ContentFile
import tempfile
import os
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

class RedditView:


    def Home(request):
        contents = ContentDB.objects.filter(platform='Reddit').order_by('-id')[:10]
        uploads = []
        for content in contents:
            print(content)
            print(content.userIcon)
            if content.image_url:
                try:
                    file = FileDB.objects.get(uid=content.image_url)
                    content.image_url = file.url
                except FileDB.DoesNotExist:
                    content.image_url = None
            upload = {
                'userID': content.userID,
                'text': content.text,
                'platform': content.platform,
                'icon' : content.userIcon,
                'image_url': content.image_url,
                'vote': content.vote
            }
            uploads.append(upload)
        return render(request, 'reddit/home.html', {'contents': uploads})
 
    def Disconnect(request):
        account = AccountDB.objects.filter(platform='Reddit').first()
        account.token = ''
        account.connected = False
        account.save()
        request.session.flush()
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

        return redirect(auth_url_full)
    
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
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            refresh_token=refresh_token
        )
    
        try:
            user = reddit.user.me()
            print("user name", user.name) 
             
            print("user profile", user.icon_img) 
            account = AccountDB.objects.filter(platform='Reddit').first()
            account.token = refresh_token
            account.name = user.name
            account.connected = True
            account.icon = user.icon_img
            account.save()

            return render(request, 'page/00_welcome2.html', parameters())
        except Exception as e:
            print(f'Failed to get user: {e}')
            RedditView.reddit = None
            return redirect('/Reddit/connect')


    def GetContent(request):
        account = AccountDB.objects.filter(platform="Reddit").first()
        print(account.token)
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            refresh_token=account.token
        )
        if reddit and reddit:
            success = Content(reddit)

            if success:
                return JsonResponse({'message': 'success get Content'})
            
            
            return JsonResponse({'error': 'Failed to get Content'}, status=400)
        return redirect('/Reddit/connect')


    # 레딧의 경우 포스팅이 제목, 이미지 혹은 제목 텍스트 만 가능
    def CreatePost(request):
        if request.method == 'POST':
            
            json_data = json.loads(request.body) # 
            print("json_data : ", json_data)
            title = json_data['title']
            text = json_data['text']
            file = json_data['file']
            print("content : " , title,"text : ", text)
            print("file : ", file)
            # base64로 인코딩된 이미지를 디코딩

            account = AccountDB.objects.filter(platform="Reddit").first()
            if account is None:
                return redirect('/Reddit/connect')
            print(account.token)
            reddit = praw.Reddit(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                user_agent=USER_AGENT,
                refresh_token=account.token
            )

            # title과 file이 있을 경우
            if title and file:
                success = Post(reddit, title, image=temp_path)
                if success:
                    return JsonResponse({"success": "Posting Image"})
            # title과 text가 있을 경우
            if title and text and file=='':
                print("title and text")
                success = Post(reddit ,title, text=text)
                if success:
                    return JsonResponse({"success": "Posting Text"})
                
                return JsonResponse({"error":"Posting failed"}, status=400)
            return JsonResponse({"error":"Posting failed, The requirements are not satisfied"}, status=400)
        return HttpResponse('Post')
    # Compare this snippet from platformReddit/views.py:


    def get_reddit_instance():
        return RedditView.reddit

