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
        return render(request, 'new_page/init.html', parameters('Start'))
    def Home(request):
        return render(request, 'new_page/home.html', parameters('Home'))
    def Search(request):
        return render(request, 'new_page/search.html', parameters('Search'))
    def Video(request):
        return render(request, 'new_page/video.html', parameters('Video'))
    def Create(request):
        return render(request, 'new_page/create.html', parameters('Create'))
    def Contacts(request):
        return render(request, 'new_page/contacts.html', parameters('Contacts'))