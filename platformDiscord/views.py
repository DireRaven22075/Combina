from django.shortcuts import render, redirect
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from page.models import ContentDB, AccountDB, FileDB
from .forms import TokenForm
from .discord_bot import DiscordBotService
from django.templatetags.static import static
import json

class DiscordBotView:
    DEFAULT_PROFILE_IMAGE_URL = '/static/img/old/discord-mark-blue.svg'

    @staticmethod
    async def fetch_discord_messages(request):
        if request.method == 'POST':
            bot_token = await sync_to_async(request.session.get)('bot_token')
            data = json.loads(request.body)
            num_messages = int(data.get('num_messages', 20))
            bot_service = DiscordBotService(bot_token)
            await bot_service.run_bot(num_messages)
            messages = await sync_to_async(list)(
                ContentDB.objects.filter(platform='discord').order_by('-id')[:num_messages].values('userID', 'userIcon', 'text', 'image_url')
            )
            for message in messages:
                if not message['userIcon']:
                    message['userIcon'] = DiscordBotView.DEFAULT_PROFILE_IMAGE_URL
                if message['image_url'] != 0:
                    try:
                        file_db = await sync_to_async(FileDB.objects.get)(uid=message['image_url'])
                        message['image_url'] = file_db.url
                    except FileDB.DoesNotExist:
                        message['image_url'] = None  # 이미지가 없는 경우 None 설정
                else:
                    message['image_url'] = None  # 이미지가 없는 경우 None 설정

            return JsonResponse({'messages': messages})
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
    def index(request):
        current_account = AccountDB.objects.filter(platform='discord').first()
        messages = ContentDB.objects.filter(platform='discord').order_by('-id')[:20]
        message_list = []
        for msg in messages:
            image_url = None
            if msg.image_url != 0:
                try:
                    file_db = FileDB.objects.get(uid=msg.image_url)
                    image_url = file_db.url
                except FileDB.DoesNotExist:
                    pass

            message_list.append({
                'text': msg.text,
                'userIcon': msg.userIcon,
                'userID': msg.userID,
                'image_url': image_url
            })

        profile_image_url = '/static/img/old/discord-mark-blue.svg'
        return render(request, 'discord_template/index.html', {
            'messages': message_list,
            'current_channel': current_account.tag if current_account else '',
            'profile_image_url': profile_image_url
        })

    @staticmethod
    async def send_discord_message(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            message = data.get('message')
            image_data = data.get('image')
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
