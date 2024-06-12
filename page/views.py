from django.shortcuts import render, redirect
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
    data['connected'] = isOkay()
    return data
def isOkay():
    for account in AccountDB.objects.all():
        if account.connected:
            return True
    return False
class PageView:
    def Welcome(request):
        if (AccountDB.objects.all().count() == 0):
            AccountDB.objects.create(platform='Facebook', connected=False)
            AccountDB.objects.create(platform='Instagram', connected=False)
            AccountDB.objects.create(platform='Discord', connected=False)
            AccountDB.objects.create(platform='Reddit', connected=False)
            AccountDB.objects.create(platform='Everytime', connected=False)
            AccountDB.objects.create(platform='Youtube', connected=False)
        
        if (request.session.get('visited') == None):
            request.session['visited'] = True
            return render(request, 'page/00_welcome1.html', {'connected': True})
        try:
            redirect('/discord/get-content')
            redirect('/reddit/get-content')
            redirect('/youtube/get-content')
            redirect('/everytime/get-content')
            redirect('/facebook/get-content')
            redirect('/instagram/get-content')
        except:
            pass

        return render(request, 'page/00_welcome1.html', parameters())
    def Welcome2(request):
        return render(request, 'page/00_welcome2.html', parameters())
    def Home(request):
        if (isOkay() == False):
            return redirect('/')
        if (request.POST.get("search") != None):
            data = parameters()
            data['contents'] = ContentDB.objects.filter(text__contains=request.POST.get("search"))
            return render(request, 'page/01_home.html', data)
        return render(request, 'page/01_home.html', parameters())
    def Contacts(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/02_contacts.html', parameters())
    def Create(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/03_create.html', parameters())
    def Accounts(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/04_accounts.html', parameters())
    def Settings(request):
        if (isOkay() == False):
            return redirect('/')
        return render(request, 'page/05_settings.html', parameters())