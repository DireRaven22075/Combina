import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from page.models import *
from page.views import *

class ServerView:
    def Disconnect(request):
        platforms = parameters()['platforms']
        cookies = {'csrftoken': get_token(request)}
        headers = {
                'Content-Type': 'application/json',
                'csrfmiddlewaretoken': get_token(request),  # 'X-CSRFToken': 'token
                'X-CSRFToken': get_token(request)
        }
        for platform in platforms:
            url = f'http://127.0.0.1:8000/{platform}/disconnect/'
            response = requests.post(url, cookies=cookies, headers=headers)
        return redirect('http://127.0.0.1:8000/accounts', cookies=cookies, headers=headers)
    
    def GetContent(request):
        platforms = parameters()['platforms']
        cookies = {
                'csrftoken': get_token(request)
        }
        headers = {
                'Content-Type': 'application/json',
                'csrfmiddlewaretoken': get_token(request),  # 'X-CSRFToken': 'token
                'X-CSRFToken': get_token(request)
        }
        for account in AccountDB.objects.all():
            if (account.connected == False):
                continue
            url = f'http://127.0.0.1:8000/{account.platform}/get-content/'
            response = requests.post(url, cookies=cookies, headers=headers)
        return redirect('http://127.0.0.1:8000/home/', cookies=cookies)
    
    def Post(request):
        if request.method == "POST":
            data = {
                "title": request.POST.get("title"),
                "text": request.POST.get("text"),
                "file": request.FILES.get("file")
            }

            headers = {
                'Content-Type': 'application/json',
                'csrfmiddlewaretoken': get_token(request),  # 'X-CSRFToken': 'token
                'X-CSRFToken': get_token(request)
            }
            
            platforms = parameters()['platforms']
            base_url = "http://localhost:8000"  # 기본 URL 설정

            for platform in platforms:
                if request.POST.get(platform):
                    url = f'{base_url}/{platform}/post/'
                    try:
                        
                        cookies = {
                            'csrftoken': get_token(request),
                        }

                        response = requests.post(url, json=data, headers=headers, cookies=cookies)
                        if response.status_code == 200:
                            print(f"Successfully posted to {platform}")
                        else:
                            print(f"Failed to post to {platform}: {response.status_code} {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"Request to {platform} failed: {e}")
            
            return redirect('http://127.0.0.1:8000/create')
        return redirect(request.META.get('HTTP_REFERER', '/home'))

    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        return redirect(request.META.get('HTTP_REFERER', '/home'))
