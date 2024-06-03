from django.shortcuts import render
from django.http import HttpResponse
from .models import *
def parameters():
    data = {}
    data['contents'] = ContentDB.objects.all()
    data['accounts'] = AccountDB.objects.all()
    print(data)
    return data
class PageView:
    def Welcome(request):
        return render(request, 'welcome.html', parameters())
    def Home(request):
        return render(request, 'home.html', parameters())
    def Menu(request):
        return render(request, 'page/menu.html', parameters())
    def Post(request):
        return render(request, 'page/post.html', parameters())