import json
from django.shortcuts import render
from django.http import JsonResponse
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
                await sync_to_async(DiscordChannel.objects.all().delete)()
                await sync_to_async(DiscordChannel.objects.create)(channel_id=channel_id)
                return JsonResponse({'success': True, 'channel_id': channel_id})
            return JsonResponse({'error': 'No channel ID provided'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    async def update_bot_profile(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            bot_name = data.get('bot_name')
            bot_avatar = data.get('bot_avatar')
            success = await update_bot_profile(bot_name, bot_avatar)
            if success:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Failed to update bot profile'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)
