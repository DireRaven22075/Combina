from django.shortcuts import render, redirect
from page.utils import driver_set
#from page.views import user
# Create your views here.

def login(request):
    
    return render(request, 'account/login.html')

def login_info(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user.login(name, password)
        if user is None:
            print("incorrect login")
        print(f"login name : {name}")
        print(f"login password : {password}")
        return redirect('/')
    return render(request, 'account/login.html')
def logout(request):
    return render(request, 'account/login.html')