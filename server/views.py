import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from page.models import *
from page.views import *

class ServerView:
    def Disconnect(request):
        for account in AccountDB.objects.all():
            account.name = ""
            account.tag = ""
            account.token = ""
            account.connected = False
            account.save()
        return redirect(request.META.get('HTTP_REFERER', '/home'))

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
            
            return HttpResponse("Post request processed")
        
        return HttpResponse("Invalid request method")

    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        return redirect(request.META.get('HTTP_REFERER', '/home'))
