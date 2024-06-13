import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from page.models import *
from page.views import *
class ServerView:
    def Post(request):
        if (request.method == "POST"):
            session = requests.Session()
            print(get_token(request))
            data = {}
            data["title"] = request.POST.get("title")
            data["target"] = request.POST.get("platform")
            data["content"] = request.POST.get("content")
            data["file"] = request.POST.get("file")
            data['csrftoken'] = get_token(request)
            headers = {
                'X-CSRFToken': get_token(request),
            }
            requests.post('http://127.0.0.1:8000/server/test/',headers=headers, data=data)
            #requests.get("/discord/post", data=data)
            requests.get("/Everytime/post", data=data)
            return redirect(request.META.get('HTTP_REFERER', '/home'))
        else:
            return HttpResponse("Invalid request method")
    def Test(request):
        data = ContentDB(
            text=request.POST.get("content"),
        )
        data.save()
        ContentDB.objects.create(content=request.POST.get("content")).save()
        return JsonResponse({"status": "success"})
    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        return redirect(request.META.get('HTTP_REFERER', '/home'))