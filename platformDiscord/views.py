from django.shortcuts import render, redirect
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import DiscordMessage, DiscordChannel
from .forms import TokenForm
from .discord_bot import DiscordBotService
import json

class DiscordBotView:
    DEFAULT_PROFILE_IMAGE_URL = '/static/discord_logo.png'
    
    @staticmethod
    async def fetch_discord_messages(request):
        if request.method == 'POST':
            bot_token = await sync_to_async(request.session.get)('bot_token')
            data = json.loads(request.body)
            num_messages = int(data.get('num_messages', 20))
            bot_service = DiscordBotService(bot_token)
            await bot_service.run_bot(num_messages)
            messages = await sync_to_async(list)(
                DiscordMessage.objects.all().order_by('-id')[:num_messages].values('author', 'author_id', 'content', 'image_url', 'profile_image_url', 'timestamp')
            )
            for message in messages:
                message['timestamp'] = message['timestamp'].isoformat()
                if not message['profile_image_url']:
                    message['profile_image_url'] = DiscordBotView.DEFAULT_PROFILE_IMAGE_URL
            return JsonResponse({'messages': messages})
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
    def index(request):
        if 'bot_token' not in request.session:
            return redirect('set_token')

        messages = DiscordMessage.objects.all().order_by('-id')
        current_channel = DiscordChannel.objects.first()
        return render(request, 'index.html', {'messages': messages, 'current_channel': current_channel.channel_id if current_channel else ''})

    @staticmethod
    async def send_discord_message(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message')
            image_data = data.get('image')  # 이미지 데이터
            bot_token = await sync_to_async(request.session.get)('bot_token')
            bot_service = DiscordBotService(bot_token)
            if message or image_data:
                success = await bot_service.send_message_to_discord(message, image_data)
                return JsonResponse({'success': success})
            return JsonResponse({'error': 'No message or image provided'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
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

    @staticmethod
    async def update_bot_profile_view(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            bot_name = data.get('bot_name')
            bot_avatar = data.get('bot_avatar')
            bot_token = await sync_to_async(request.session.get)('bot_token')
            bot_service = DiscordBotService(bot_token)
            success = await bot_service.update_bot_profile(bot_name, bot_avatar)
            if success:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Failed to update bot profile'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
    def set_token(request):
        if request.method == 'POST':
            form = TokenForm(request.POST)
            if form.is_valid():
                request.session['bot_token'] = form.cleaned_data['bot_token']
                return redirect('index')
        else:
            form = TokenForm()
        return render(request, 'set_token.html', {'form': form})
