from django.shortcuts import render
from django.http import HttpResponse
from page.models import *
from page.views import *
class ServerView:
    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        return HttpResponse('ClearContent')
    
    def Disconnect(request):
        if (request.method == "POST"):
            target = request.POST.get("platform")
            AccountDB.objects.filter(target).update(connected=False)
    
    def Connect(request):
        if (request.method == "POST"):
            target = request.POST.get("platform")
            token = request.POST.get("token")
            name = request.POST.get("name")
            tag = request.POST.get("tag")
            AccountDB.objects.filter(target).update(token=token)
            AccountDB.objects.filter(target).update(name=name)
            AccountDB.objects.filter(target).update(tag=tag)
            AccountDB.objects.filter(target).update(connected=True)
            return HttpResponse('Connected')

    def ClearAccount(request):
        AccountDB.objects.all().update(connected=False)
        AccountDB.objects.all().update(id="")
        AccountDB.objects.all().update(token="")
        AccountDB.objects.all().update(name="")
        AccountDB.objects.all().update(tag="")
        return HttpResponse('ClearAccount')
    def InitAccount(request):
        for i in AccountDB.objects.all():
            i.connected = False
            i.save()