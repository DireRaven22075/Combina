from django.shortcuts import render, redirect
from django.http import HttpResponse
import praw
from page.models import *
data = {
    "client_id": "a-TpD_hJiCllSc7JG3seaA",
    "client_secret": 'grifUSnHoHW5n8Y-bATjE3DsQmNoTg',
    "user_agent": 'Combina-webengine_v1.0',
    "credentials_file": 'credentials.json',
}
class RedditView:
    def Disconnect(request):
        account = AccountDB.objects.filter(platform='Reddit').first()
        account.token = ''
        account.connected = False
        account.save()
        if (request.POST.get('page') == 'welcome2'):
            return redirect('/start')
        else:
            return redirect('/accounts')
    def Connect(request):
        return render(request, 'reddit/login.html')
    def ConnectCall(request):
        if (request.method == 'POST'):
            name = request.POST.get('username')
            password = request.POST.get('password')
            try:
                reddit = praw.Reddit(client_id=data['client_id'],
                                        client_secret=data['client_secret'],
                                        user_agent=data['user_agent'],
                                        username=name,
                                        password=password)
                account = AccountDB.objects.filter(platform='Reddit').first()
                account.token = reddit.auth.
                account.name = reddit.user.me().name
                account.connected = True
                account.save()
            except Exception as e:
                print(f'Failed to login: {e}')
            if (request.POST.get('page') == 'welcome2'):
                return redirect('/start')
            else:
                return redirect('/accounts')
    def GetContent(request):
        account = AccountDB.objects.filter(platform='Reddit').first()
        return HttpResponse('GetContent')
    def Post(request):
        return HttpResponse('Post')
    # Compare this snippet from platformReddit/views.py:
