from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from page.models import *
# Create your views here.

class YoutubeView:
    def Connect(request):


        return HttpResponse("test")

    def Disconnect(request):
        return redirect(request.META.get('HTTP_REFERER'), "/home/")