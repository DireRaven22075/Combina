import base64
from io import BytesIO
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from asgiref.sync import sync_to_async
from page.models import ContentDB, AccountDB, FileDB
from .forms import TokenForm
from .discord_bot import DiscordBotService
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
import requests  # requests 모듈 임포트
import discord

class DiscordBotView:
    # 디스코드의 기본 프로필 이미지 URL 설정
    DEFAULT_PROFILE_IMAGE_URL = '/static/img/old/discord-mark-blue.svg'

    @csrf_exempt
    async def get_content(request):
        if request.method in ['GET', 'POST']:
            try:
                num_messages = 20
                if request.method == 'POST':
                    body = request.body.decode('utf-8')
                    data = json.loads(body)
                    num_messages = int(data.get('num_messages', 20))
                else:
                    num_messages = int(request.GET.get('num_messages', 20))

                if num_messages <= 0:
                    return HttpResponseBadRequest('num_messages must be a positive integer')

                # 데이터베이스에서 봇 토큰 가져오기
                account = await sync_to_async(AccountDB.objects.filter(platform='Discord').first)()
                if not account or not account.token:
                    return JsonResponse({'error': 'Bot token not found in database'}, status=400)
                bot_token = account.token

                bot_service = DiscordBotService(bot_token, account.tag, discord.Intents.default())
                messages = await bot_service.fetch_messages_from_discord(num_messages)

                response_data = []
                for message in messages:
                    response_data.append({
                        'userID': message.author.name,
                        'userIcon': str(message.author.display_avatar.url) if message.author.display_avatar else 'http://default.url/icon.png',
                        'text': message.content,
                        'image_url': message.attachments[0].url if message.attachments else None
                    })

                return JsonResponse({'messages': response_data})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return HttpResponseBadRequest('Invalid request method')

    @staticmethod
    def index(request):
        """
        디스코드 메시지를 보여주는 기본 페이지
        - 현재 계정을 가져오고, 최신 메시지 20개를 가져옴
        - 각 메시지의 이미지 URL을 파일 데이터베이스에서 확인하여 리스트로 변환
        """
        # 현재 계정 정보 가져오기
        current_account = AccountDB.objects.filter(platform='discord').first()
        # 최신 메시지 20개 가져오기
        messages = ContentDB.objects.filter(platform='discord').order_by('-id')[:20]
        message_list = []
        for msg in messages:
            image_url = None
            # 이미지 URL 확인 및 파일 데이터베이스에서 URL 가져오기
            if msg.image_url != 0:
                try:
                    file_db = FileDB.objects.get(uid=msg.image_url)
                    image_url = file_db.url
                except FileDB.DoesNotExist:
                    pass
            # 메시지 정보를 리스트에 추가
            message_list.append({
                'text': msg.text,
                'userIcon': msg.userIcon,
                'userID': msg.userID,
                'image_url': image_url
            })

        # 기본 프로필 이미지 URL 설정
        profile_image_url = '/static/img/old/discord-mark-blue.svg'
        # 메시지와 채널 정보를 템플릿에 전달하여 렌더링
        return render(request, 'discord_template/index.html', {
            'messages': message_list,
            'current_channel': current_account.tag if current_account else '',
            'profile_image_url': profile_image_url
        })

    @csrf_exempt
    async def send_discord_message(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                title = data.get('title', 'No Title')
                text = data.get('text', '')
                files = data.get('files', [])

                # 데이터베이스에서 봇 토큰 가져오기
                account = await sync_to_async(AccountDB.objects.filter(platform='Discord').first)()
                if not account or not account.token:
                    return JsonResponse({'error': 'Bot token not found in database'}, status=400)
                bot_token = account.token

                bot_service = DiscordBotService(bot_token, account.tag, discord.Intents.default())
                message_content = f"**{title}**\n\n{text}"

                if files:
                    image_data = base64.b64encode(files[0]['data'].encode()).decode() if files else None
                    await bot_service.send_message_to_discord(message_content, image_data)
                else:
                    await bot_service.send_message_to_discord(message_content)

                return JsonResponse({'success': True})
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON format')
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
    async def set_channel_id(request):
        """
        디스코드 채널 ID를 설정하는 함수
        - POST 요청을 받아 채널 ID를 데이터베이스에 저장
        """
        if request.method == 'POST':
            # 요청 데이터 파싱
            data = json.loads(request.body)
            channel_id = data.get('channel_id')
            if channel_id:
                # 현재 계정 정보 가져오기
                account = await sync_to_async(AccountDB.objects.filter(platform='discord').first)()
                if account:
                    account.tag = channel_id
                    await sync_to_async(account.save)()
                else:
                    # 계정이 없는 경우 새로 생성
                    await sync_to_async(AccountDB.objects.create)(
                        platform='discord',
                        tag=channel_id
                    )
                return JsonResponse({'success': True, 'channel_id': channel_id})
            return JsonResponse({'error': 'No channel ID provided'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
    async def update_bot_profile_view(request):
        """
        디스코드 봇의 프로필을 업데이트하는 함수
        - POST 요청을 받아 봇의 이름과 아바타를 업데이트
        """
        if request.method == 'POST':
            # 요청 데이터 파싱
            data = json.loads(request.body)
            bot_name = data.get('bot_name')
            bot_avatar = data.get('bot_avatar')
            # 세션에서 봇 토큰 가져오기
            bot_token = await sync_to_async(request.session.get)('bot_token')
            bot_service = DiscordBotService(bot_token)
            # 봇 프로필 업데이트 수행
            success = await bot_service.update_bot_profile(bot_name, bot_avatar)
            if success:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Failed to update bot profile'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    @staticmethod
    @csrf_exempt
    def connect(request):
        if request.method == 'POST':
            try:
                body = request.body.decode('utf-8')
                data = json.loads(body)
                bot_token = data.get('bot_token')
                return_url = data.get('return_url', '/')

                if bot_token:
                    try:
                        bot_info = get_bot_info(bot_token)
                        name = bot_info.get("name")
                        icon = bot_info.get("icon")
                    except Exception as e:
                        return JsonResponse({'error': str(e)}, status=400)

                    account, created = AccountDB.objects.get_or_create(platform='Discord')
                    account.token = bot_token
                    account.name = name
                    account.icon = icon
                    account.connected = True
                    account.save()

                    # 세션에 봇 토큰 저장
                    request.session['bot_token'] = bot_token

                    return JsonResponse({
                        'redirect_url': return_url,
                        'connection': True
                    })
                else:
                    return JsonResponse({'error': 'Bot token is required'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            form = TokenForm()
            return_url = request.GET.get('return_url', '/')
            request.session['return_url'] = return_url
            return render(request, 'discord_template/connect.html', {
                'form': form,
                'return_url': return_url
            })

# 디스코드 봇 정보 가져오기 함수
def get_bot_info(bot_token):
    url = "https://discord.com/api/v9/users/@me"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("username"),
            "icon": f'https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.png'
        }
    else:
        raise Exception("Failed to get bot info from Discord API")

class RedirectPageView(View):
    def post(self, request, *args, **kwargs):
        """
        페이지 리다이렉트를 처리하는 함수
        - POST 요청을 받아 'page' 파라미터에 따라 다른 URL로 리다이렉트.
        """
        try:
            data = json.loads(request.body)
            page = data.get('page', 'init')

            if page == 'account':
                return redirect('http://127.0.0.1/account')
            else:
                return redirect('http://127.0.0.1')
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

class PostAccountView(View):
    def post(self, request, *args, **kwargs):
        """
        계정 정보를 POST로 처리하는 함수
        - 'account' 파라미터를 받아 True일 경우 성공 메시지 반환
        """
        try:
            data = json.loads(request.body)
            account = data.get('account', False)
            
            if account:
                return JsonResponse({'success': True})
            else:
                return HttpResponseBadRequest('Account value not provided')
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON')

class DisconnectView(View):
    @method_decorator(csrf_exempt)
    def get(self, request):
        """
        플랫폼 연결 해제.
        - GET 요청을 받아 처리할 수 있도록 함.
        - 관련된 모든 세션 데이터를 삭제.
        - connected 상태를 False로 설정.
        """
        account = AccountDB.objects.filter(platform='discord').first()
        if account:
            account.name = ''
            account.connected = False  # connected 값을 False로 설정
            account.token = ''  # 봇 토큰 초기화
            account.save()

        # 세션 데이터 삭제
        keys_to_delete = ['bot_token', 'platform_channel_id', 'platform_messages']
        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]    
        return redirect(request.META.get('HTTP_REFERER', '/'))

class ConnectView(View):
    def get(self, request):
        """
        플랫폼 연동을 위한 페이지를 반환.
        - GET 요청에서 `return_url` 파라미터를 받아 세션에 저장.
        """
        return_url = request.GET.get('return_url', '/')
        request.session['return_url'] = return_url
        return render(request, 'platform_template/connect.html', {
            'form': TokenForm(),
            'return_url': return_url,
        })

    def post(self, request):
        """
        POST 요청에서 토큰을 받아 저장하고 원래 페이지로 리다이렉트.
        """
        form = TokenForm(request.POST)
        if form.is_valid():
            request.session['bot_token'] = form.cleaned_data['bot_token']
            redirect_url = request.session.get('return_url', '/')
            return JsonResponse({
                'redirect_url': redirect_url,
                'connection': True  # connection 값을 True로 설정
            })
        return JsonResponse({'error': 'Invalid form data'}, status=400)
