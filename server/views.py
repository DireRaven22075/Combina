from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def Post(request):
    return HttpResponse("<pre>" + request.POST.get('content') + "</pre>")

def Disconnect(request):
    return render(request, 'menu.html', json={'status': request.POST.get('status')})