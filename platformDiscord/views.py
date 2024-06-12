from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from asgiref.sync import sync_to_async
from page.models import ContentDB, AccountDB, FileDB
from .forms import TokenForm
from .discord_bot import DiscordBotService
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from . import settings as discord_settings
import json

class DiscordBotView:
    # 디스코드의 기본 프로필 이미지 URL 설정
    DEFAULT_PROFILE_IMAGE_URL = '/static/img/old/discord-mark-blue.svg'

    @csrf_exempt
    async def get_content(request):
        """
        디스코드 메시지를 가져오는 함수
        - GET 또는 POST 요청을 처리하여 메시지를 가져옴
        - num_messages 파라미터로 가져올 메시지 개수를 결정
        - 메시지를 가져와 JSON으로 반환
        """
        if request.method == 'POST' or request.method == 'GET':
            if request.method == 'POST':
                try:
                    body = request.body.decode('utf-8')
                    if not body:
                        return HttpResponseBadRequest('Empty request body')

                    data = json.loads(body)
                except json.JSONDecodeError:
                    return HttpResponseBadRequest('Invalid JSON format')
                
                num_messages = data.get('num_messages', 20)
            else:
                num_messages = request.GET.get('num_messages', 20)

            bot_token = await sync_to_async(request.session.get)('bot_token')
            if not bot_token:
                return JsonResponse({'error': 'Bot token not found in session'}, status=400)

            bot_service = DiscordBotService(bot_token)
            await bot_service.run_bot(int(num_messages))

            messages = await sync_to_async(list)(
                ContentDB.objects.filter(platform='discord').order_by('-id')[:int(num_messages)].values('userID', 'userIcon', 'text', 'image_url')
            )

            for message in messages:
                if not message['userIcon']:
                    message['userIcon'] = '/static/img/old/discord-mark-blue.svg'
                if message['image_url'] != 0:
                    try:
                        file_db = await sync_to_async(FileDB.objects.get)(uid=message['image_url'])
                        message['image_url'] = file_db.url
                    except FileDB.DoesNotExist:
                        message['image_url'] = None
                else:
                    message['image_url'] = None

            return JsonResponse({'messages': messages})
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

    @staticmethod
    async def send_discord_message(request):
        """
        디스코드 채널로 메시지 또는 이미지를 전송하는 함수
        - POST 요청을 받아 메시지와 이미지를 디스코드로 전송
        """
        if request.method == 'POST':
            # 요청 데이터 파싱
            data = json.loads(request.body)
            message = data.get('message')
            image_data = data.get('image')
            # 세션에서 봇 토큰 가져오기
            bot_token = await sync_to_async(request.session.get)('bot_token')
            bot_service = DiscordBotService(bot_token)
            # 메시지나 이미지가 있는 경우 전송
            if message or image_data:
                success = await bot_service.send_message_to_discord(message, image_data)
                return JsonResponse({'success': success})
            return JsonResponse({'error': 'No message or image provided'}, status=400)
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
    def connect(request):
        """
        디스코드 봇 토큰을 설정하고 리다이렉트하는 함수
        - POST 요청을 통해 봇 토큰을 설정하고 원래 페이지로 리다이렉트.
        """
        if request.method == 'POST':
            try:
                body = request.body.decode('utf-8')
                data = json.loads(body)
                bot_token = data.get('bot_token')
                return_url = data.get('return_url', '/')
                if bot_token:
                    request.session['bot_token'] = bot_token
                    return JsonResponse({
                        'redirect_url': return_url,
                        'connection': True  # connection 값을 True로 설정
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
    def post(self, request):
        """
        플랫폼 연결 해제.
        - 관련된 모든 세션 데이터를 삭제.
        - 성공 메시지 반환.
        """
        keys_to_delete = ['bot_token', 'discord_channel_id', 'discord_messages']
        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]
        
        return JsonResponse({'success': True, 'message': 'Disconnected and cleared all Discord related data.'})

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
