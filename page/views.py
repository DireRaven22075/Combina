from django.shortcuts import render
from django.http import HttpResponse
from . import sql, func
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
            "text": "TTTT",
            "image": "https://cdn.mos.cms.futurecdn.net/2aeE963L5B7jnfCAWFoFYW-1920-80.jpg.webp"
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
            "text": "TTTT",
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
def Welcome(request):
    return render(request, 'home.html', parameters)
def Home(request):
    return render(request, 'home.html', parameters)
def Post(request):
    return render(request, 'post.html', parameters)
def Find(request):
    return render(request, 'find.html', parameters)
def Menu(request):
    return render(request, 'menu.html', parameters)