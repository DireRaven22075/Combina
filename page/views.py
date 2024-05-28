from django.shortcuts import render
from django.http import HttpResponse
from . import sql
DEBUG = True
parameters = {
    "chats": [
        {
            "icon": "https://www.facebook.com/images/fb_icon_325x325.png",
            "target": "한철연",
            "topMessage": "뭐함",
            "time": "2020-01-01 12:00:00",
            "unread": 3
        },
        {
            "target": "한철연",
            "topMessage": "뭐함",
            "time": "2020-01-01 12:00:00",
            "unread": 3
        },
        {
            "target": "한철연",
            "topMessage": "뭐함",
            "time": "2020-01-01 12:00:00",
            "unread": 3
        },
        {
            "target": "한철연",
            "topMessage": "뭐함",
            "time": "2020-01-01 12:00:00",
            "unread": 3
        },
        {
            "target": "한철연",
            "topMessage": "뭐함",
            "time": "2020-01-01 12:00:00",
            "unread": 3
        },
    ],
    "contents" : [
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT"
        },
        
        {
            "platform": "Instagram",
            "text": "FADAS"
        }
    ],
    "accounts": [
        {
            "connected": 1,
            "platform": "Facebook",
            "id": "gskids053",
            "name": "DireRaven22075",
            "tag": "hanyoonsoo"
        },
        {
            "connected": 1,
            "platform": "Instagram",
            "id": 2,
            "name": "DireRaven22075",
            "tag": "hanyoonsoo"
        }
    ]
}

def Home(request):
    parameters = {}
    data = sql.Account.getData()

    return render(request, 'home.html', parameters)

def Post(request):
    return render(request, 'post.html', parameters)

def Find(request):
    return render(request, 'find.html', parameters)

def Chat(request):
    return render(request, 'chat.html', parameters)

def InChat(request, platform, id):
    return render(request, 'inChat.html', parameters)

def Menu(request):
    return render(request, 'menu.html', parameters)

def DBTest(request):
    result = sql.get_account()
    return HttpResponse(result)

def Disconnect(request):
    return HttpResponse(request.POST.get('id'))
    if request.method == 'POST':
            # Access the POST data
        post_data = request.POST

            # Process the POST data
            # ...

        return HttpResponse('POST request processed successfully')
    else:
        return HttpResponse('Only POST requests are allowed')
    return HttpResponse(request.POST.get('id'))
    def MyView(request):
        if request.method == 'POST':
            # Access the POST data
            post_data = request.POST

            # Access specific POST parameters
            param1 = post_data.get('param1')
            param2 = post_data.get('param2')

            # Process the POST data
            # ...

            return HttpResponse('POST request processed successfully')
        else:
            return HttpResponse('Only POST requests are allowed')