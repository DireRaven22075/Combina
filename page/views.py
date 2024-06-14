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
    data['files'] = FileDB.objects.all()
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
            AccountDB.objects.filter(platform='Youtube').first().token = '{"installed":{"client_id":"1093025684898-1kdj5micd00haaeo3g0kr9n9fep49fev.apps.googleusercontent.com","project_id":"combina-youtube","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}'
            AccountDB.objects.filter(platform='Youtube').first().save()
        
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