from django.shortcuts import render, redirect
from django.http import HttpResponse
import praw
import requests
from page.models import *
CLIENT_ID = 'a-TpD_hJiCllSc7JG3seaA'
CLIENT_SECRET = 'grifUSnHoHW5n8Y-bATjE3DsQmNoTg'
USER_AGENT = 'Combina-webengine_v1.0'

class RedditView:
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
        return render(request, 'reddit/login.html')
    def Callback(request):
        code = request.GET.get('code')
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
        post_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:8000/Reddit/callback',
        }
        headers = {
            'User-Agent': USER_AGENT
        }
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                                auth=auth, data=post_data, headers=headers)
        print(response.json())
        return redirect('/Reddit/connect?code=' + code)
    def ConnectCall(request):
        if (request.method == 'POST'):
            name = request.POST.get('username')
            password = request.POST.get('password')
            code = request.GET.get('code')
            auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
            post_data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'http://localhost:8000/Reddit/callback',
            }
            headers = {
                'User-Agent': USER_AGENT
            }
            response = requests.post('https://www.reddit.com/api/v1/access_token',
                                    auth=auth, data=post_data, headers=headers)
            print(response.json())
            if (request.POST.get('page') == 'welcome2'):
                return redirect('/start')
            else:
                return redirect('/accounts')
    def GetContent(request):
        account = AccountDB.objects.filter(platform='Reddit').first()
        return HttpResponse('GetContent')
    def Post(request):
        return HttpResponse('Post')
    # Compare this snippet from platformReddit/views.py:
