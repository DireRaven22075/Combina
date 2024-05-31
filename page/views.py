from django.shortcuts import render
from django.http import HttpResponse
from . import sql
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
class Server:
    def Post(request):
        return HttpResponse(request.POST.get('title'))
def Home(request):
    data = {}
    accounts = sql.Account.getData()
    data['accounts'] = accounts
    return render(request, 'home.html', data)

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

def DBINIT(request):
    sql.Account.deleteDataAll()
    sql.Account.addData('Facebook', 'gskids053')
    return render(request, 'menu.html', parameters)
def DBTest(request):
    result = sql.get_account()
    sql.Account.test()
    return HttpResponse(result)


def Disconnect(request):
    platform = request.POST.get('platform')
    sql.Account.deleteData(platform)
    return render(request, 'menu.html', parameters)

#discord

import json
from django.http import JsonResponse
from django.shortcuts import render
from asgiref.sync import sync_to_async
from django.views import View
from .discord_bot import run_bot, send_message_to_discord, update_bot_profile
from .models import DiscordMessage, DiscordChannel

class DiscordView(View):
    async def fetch_discord_messages(request):
        if request.method == 'POST':
            await run_bot()
            messages = await sync_to_async(list)(DiscordMessage.objects.all().order_by('-id').values('author', 'content'))
            return JsonResponse({'messages': messages})
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    def index(request):
        messages = DiscordMessage.objects.all().order_by('-id')
        current_channel = DiscordChannel.objects.first()
        return render(request, 'index.html', {'messages': messages, 'current_channel': current_channel.channel_id if current_channel else ''})

    async def send_discord_message(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message')
            if message:
                success = await send_message_to_discord(message)
                return JsonResponse({'success': success})
            return JsonResponse({'error': 'No message provided'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    async def set_channel_id(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            channel_id = data.get('channel_id')
            if channel_id:
                await sync_to_async(DiscordChannel.objects.all().delete)()  # 이전 채널 ID 삭제
                await sync_to_async(DiscordChannel.objects.create)(channel_id=channel_id)
                return JsonResponse({'success': True, 'channel_id': channel_id})
            return JsonResponse({'error': 'No channel ID provided'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    async def update_bot_profile(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            bot_name = data.get('bot_name')
            bot_avatar = data.get('bot_avatar')  # base64로 인코딩된 이미지 데이터
            success = await update_bot_profile(bot_name, bot_avatar)
            if success:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Failed to update bot profile'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)
