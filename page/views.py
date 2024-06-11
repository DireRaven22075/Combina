from django.shortcuts import render
from django.http import HttpResponse
from .models import *
def parameters():
    data = {}
    data['platforms'] = [
        "Facebook", "Instagram", "Discord",
        "Reddit", "Everytime", "Youtube"
    ]
    data['contents'] = ContentDB.objects.all()
    data['accounts'] = AccountDB.objects.all()
    return data
class PageView:
    def Welcome(request):
        if (AccountDB.objects.all().count() == 0):
            AccountDB.objects.create(platform='Facebook', connected=False)
            AccountDB.objects.create(platform='Instagram', connected=False)
            AccountDB.objects.create(platform='Discord', connected=False)
            AccountDB.objects.create(platform='Reddit', connected=False)
            AccountDB.objects.create(platform='Everytime', connected=False)
            AccountDB.objects.create(platform='Youtube', connected=False)
        return render(request, 'page/00_welcome.html', parameters())
    def Home(request):
        return render(request, 'page/01_home.html', parameters())
    def Contacts(request):
        return render(request, 'page/02_contacts.html', parameters())
    def Create(request):
        return render(request, 'page/03_create.html', parameters())
    def Accounts(request):
        return render(request, 'page/04_accounts.html', parameters())
    def Settings(request):
        return render(request, 'page/05_settings.html', parameters())