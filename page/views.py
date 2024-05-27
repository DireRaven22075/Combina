from django.shortcuts import render

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
            "id": 1,
            "name": "John Doe",

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
