from django.shortcuts import render, redirect
from page.models import AccountDB, ContentDB
from platformEverytime.views import driver_set

def login(request):
    if request.method == "POST":
        id = request.POST.get("id")
        password = request.POST.get("password")
        print(f"id : {id}, password : {password}")
        if id is not None and password is not None:
            print("login start in login")
            auth = driver_set(request=request) 
            print("auth")
            cookies = auth.login(id=id, pw=password)
            print(f"cookies : {cookies}")
            print(f"in account view : {request.session['id'], request.session['password'], request.session['name']}")
            if cookies is not None:
                print("login success")
                try:
                    exist = AccountDB.objects.filter(name = auth.name)
                    exist.update(connected=True)
                    print("existing user")
                except AttributeError:
                    print("create new user")
                    user = AccountDB.objects.create(
                        platform = "everytime",
                        token = cookies,
                        name = auth.name,
                        tag = cookies,
                        connected = True,
                    )
                    user.save()

                return redirect('/')
            else:
                print("login error, Not cookie")
        else:
            print("login error, wrong password")
            

    return render(request, "every/login.html")

def logout(request):
    auth = driver_set(request=request)
    auth.close_driver()
    return redirect('/')
