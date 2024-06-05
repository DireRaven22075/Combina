from django.shortcuts import render
from platformEverytime.utils import driver_set
from page.models import AccountDB, ContentDB

auth = driver_set()

def home(request):
    user_info = auth.login('haneol0157', 'hayeon0157')
    print(f"auth : {auth.__str__()}")
    
    user = AccountDB.objects.create(
        platform = "everytime",
        token = user_info['cookies'],
        name = user_info['name'],
        tag = "default",
        connected = True
    )
    user.save()
    print(f"user name : {user.name}")
    #list = []
    # list = auth.free_field()

    
    # for i, post in enumerate(list, start=1):
    #     print(f"post{i} : {post}")
    return render(request, "/every/test.html")

def search(request):
    if request.method == 'POST':
        