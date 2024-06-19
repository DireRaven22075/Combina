from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
def platforms():
    return ["Reddit", "Youtube", "Everytime"]
def parameters():
    data = {}
    data['platforms'] = platforms()
    data['contents'] = ContentDB.objects.all()
    data['accounts'] = AccountDB.objects.all()
    data['files'] = FileDB.objects.all()
    data['connected'] = isOkay()
    data['setting'] = Setting.objects.all().first()
    return data
def isOkay():
    for account in AccountDB.objects.all():
        if account.connected:
            return True
    return False
class PageView:
    def Welcome(request):
        if (Setting.objects.all().count() == 0):
            setting = Setting()
            setting.save()
        if (AccountDB.objects.all().count() == 0):
            for platform in platforms():
                account = AccountDB(connected=False)
                account.platform = platform
                account.save()
        return render(request, 'page/00_welcome1.html', parameters())
    def Welcome2(request):
        return render(request, 'page/00_welcome2.html', parameters())
    def Home(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/01_home.html', parameters())
    def Create(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/02_create.html', parameters())
    def Accounts(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/03_accounts.html', parameters())
    def Settings(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/04_settings.html', parameters())