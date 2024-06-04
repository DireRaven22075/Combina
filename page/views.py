from django.shortcuts import render
from django.http import HttpResponse
from .models import *
def parameters():
    data = {}
    data['platforms'] = [
        "Facebook",
        "Instagram",
        "X",
        "Discord",
        "Reddit",
        "Everytime",
        "Youtube"
    ]
    data['contents'] = ContentDB.objects.all()
    data['accounts'] = AccountDB.objects.all()
    return data
class PageView:
    def Welcome(request):
        return render(request, 'page/init.html', parameters())
    def Home(request):
        return render(request, 'page/home.html', parameters())
    def Menu(request):
        return render(request, 'page/menu.html', parameters())
    def Post(request):
        return render(request, 'page/post.html', parameters())