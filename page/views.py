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
        if (AccountDB.objects.all().count() == 0):
            AccountDB.objects.create(platform='Facebook', connected=False)
            AccountDB.objects.create(platform='Instagram', connected=False)
            AccountDB.objects.create(platform='Discord', connected=False)
            AccountDB.objects.create(platform='Reddit', connected=False)
            AccountDB.objects.create(platform='Everytime', connected=False)
            AccountDB.objects.create(platform='Youtube', connected=False)
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
    def Accounts(request):
        return render(request, 'page/accounts.html', parameters('Accounts'))
    def Settings(request):
        return render(request, 'page/settings.html', parameters('Settings'))
    def Test(request):
        AccountDB.objects.create(platform='Facebook', token='Test', name='Test', tag='Test', connected=True)
        return HttpResponse('Test')