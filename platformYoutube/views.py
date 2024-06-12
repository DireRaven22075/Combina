from django.shortcuts import render, redirect
from page.models import *
# Create your views here.
class YoutubeView:
    def Disconnect(request):
        data = AccountDB.objects.filter(platform='Youtube').first()
        data.name = ""
        data.tag = ""
        data.token = ""
        data.connected = False
        data.save()
        return redirect(request.META.get('HTTP_REFERER'), '/home')