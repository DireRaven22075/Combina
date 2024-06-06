from django.shortcuts import render
from .utils import driver_set
# Create your views here.



user = driver_set()



def home(request):
    
    return render(request, 'page/home.html')

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        print(f"search content : {search}")

    return render(request, 'page/home.html')