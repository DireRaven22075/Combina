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
            data["text"] = request.POST.get("text")
            data['file'] = request.FILES.get("file")
            try:
                if (request.POST.get("Facebook") != None):
                    redirect('/Facebook/post', data=data)
                if (request.POST.get("Instagram") != None):
                    redirect('/Instagram/post', data=data)
                if (request.POST.get("Discord") != None):
                    redirect('/Discord/post', data=data)
                if (request.POST.get("Reddit") != None):
                    redirect('/Reddit/post', data=data)
                if (request.POST.get("Everytime") != None):
                    redirect('/Everytime/post', data=data)
                if (request.POST.get("Youtube") != None):
                    redirect('/Youtube/post', data=data)
            except:
                return redirect('/create', data={"status": "error"})
            return redirect('/create', data={"status": "success"})
        else:
            return HttpResponse("Invalid request method")
    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        return redirect(request.META.get('HTTP_REFERER', '/home'))