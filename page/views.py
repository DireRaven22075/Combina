from django.shortcuts import render
from django.http import HttpResponse
from .models import *
def parameters():
    data = {}
    data['contents'] = ContentDB.objects.all()
    data['accounts'] = AccountDB.objects.all()
class PageView:
    def Welcome1(request):
        request.session['visited'] = True
        return render(request, 'welcome/welcome1.html')
    def Welcome(request):
        if ('visited' not in request.session):
            return render(request, 'welcome/welcome1.html')
        else:
            return render(request, 'home.html', parameters())
    def Home(request):
        return render(request, 'home.html', parameters())
    def Post(request):
        return render(request, 'post.html', parameters())
    def Menu(request):
        return render(request, 'menu.html', parameters())