from django.shortcuts import render, redirect
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from page.models import ContentDB, AccountDB  # 모델 참조 업데이트
from .forms import TokenForm
from .discord_bot import DiscordBotService
from django.templatetags.static import static
import json

class DiscordBotView:
    DEFAULT_PROFILE_IMAGE_URL = 'img/icon/logo/discord-mark-blue.svg'

    @staticmethod
    async def fetch_discord_messages(request):
        if request.method == 'POST':
            bot_token = await sync_to_async(request.session.get)('bot_token')
            data = json.loads(request.body)
            num_messages = int(data.get('num_messages', 20))
            bot_service = DiscordBotService(bot_token)
            await bot_service.run_bot(num_messages)
            messages = await sync_to_async(list)(
                ContentDB.objects.filter(platform='discord').order_by('-id')[:num_messages].values('name', 'author_id', 'text', 'image_url', 'profile_image_url', 'time')
            )
            for message in messages:
                message['time'] = message['time'].isoformat()
                if not message['profile_image_url']:
                    message['profile_image_url'] = DiscordBotView.DEFAULT_PROFILE_IMAGE_URL

                # 필드 이름 변경
                message['author'] = message.pop('name')
                message['content'] = message.pop('text')

            # print(messages)  # 디버깅 하려고 만든 거
            return JsonResponse({'messages': messages})
        return JsonResponse({'error': 'Invalid request method'}, status=400)



    @staticmethod
    def index(request):
        messages = ContentDB.objects.all().order_by('-time')[:20]
        profile_image_url = static('img/icon/logo/discord-mark-blue.svg')
        return render(request, 'discord_template/index.html', {
            'messages': messages,
            'profile_image_url': profile_image_url,
            'current_channel': request.GET.get('channel_id', '')
        })

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
                account = await sync_to_async(AccountDB.objects.filter(platform='discord').first)()
                if account:
                    account.tag = channel_id
                    await sync_to_async(account.save)()
                else:
                    await sync_to_async(AccountDB.objects.create)(
                        platform='discord',
                        tag=channel_id
                    )
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
        return render(request, 'discord_template/set_token.html', {'form': form})
