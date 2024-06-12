import requests
from django.shortcuts import render
from django.shortcuts import redirect
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
        if (request.method == "POST"):
            session = requests.Session()
            print(get_token(request))
            data = {}
            data["title"] = request.POST.get("title")
            data["content"] = request.POST.get("content")
            if (request.POST.get("Facebook") != None):
                redirect('/facebook/post', data=data)
            if (request.POST.get("Instagram") != None):
                redirect('/instagram/post', data=data)
            if (request.POST.get("Discord") != None):
                redirect('/discord/post', data=data)
            if (request.POST.get("Reddit") != None):
                redirect('/reddit/post', data=data)
            if (request.POST.get("Everytime") != None):
                redirect('/everytime/post', data=data)
            if (request.POST.get("Youtube") != None):
                redirect('/youtube/post', data=data)
            return redirect(request.META.get('HTTP_REFERER', '/home'))
        else:
            return HttpResponse("Invalid request method")
    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        return redirect(request.META.get('HTTP_REFERER', '/home'))