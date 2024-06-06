from django.shortcuts import render
from django.http import HttpResponse
from .models import *
def parameters(name):
    data = {}
    data['platforms'] = [
        "Facebook",
        "Instagram",
        "Discord",
        "Reddit",
        "Everytime",
        "Youtube"
    ]
    data['contents'] = ContentDB.objects.all()
    data['accounts'] = AccountDB.objects.all()
    data['page'] = name
    return data
class PageView:
    def Init(request):
        return render(request, 'page/init.html', parameters('Start'))
    def Home(request):
        return render(request, 'page/home.html', parameters('Home'))
    def Explore(request):
        return render(request, 'page/explore.html', parameters('Explore'))
    def Watch(request):
        return render(request, 'page/watch.html', parameters('Watch'))
    def Contacts(request):
        return render(request, 'page/contacts.html', parameters('Contacts'))
    def Create(request):
        return render(request, 'page/create.html', parameters('Create'))