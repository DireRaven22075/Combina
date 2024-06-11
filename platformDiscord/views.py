from django.shortcuts import render, redirect
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from page.models import ContentDB, AccountDB, FileDB
from .forms import TokenForm
from .discord_bot import DiscordBotService
from django.templatetags.static import static
import json

class DiscordBotView:
    # 디스코드의 기본 프로필 이미지 URL 설정
    DEFAULT_PROFILE_IMAGE_URL = '/static/img/old/discord-mark-blue.svg'

    @staticmethod
    async def fetch_discord_messages(request):
        """
        비동기로 디스코드 메시지를 가져오는 함수
        - POST 요청을 받으면 세션에서 봇 토큰을 가져옴
        - DiscordBotService를 사용해 지정된 수만큼의 메시지를 가져옴
        - ContentDB에서 가져온 메시지를 리스트로 변환하여 JSON으로 반환
        """
        if request.method == 'POST':
            # 세션에서 봇 토큰 가져오기
            bot_token = await sync_to_async(request.session.get)('bot_token')
            # 요청 데이터 파싱
            data = json.loads(request.body)
            # 기본으로 가져올 메시지 수 설정 (기본값 20)
            num_messages = int(data.get('num_messages', 20))
            bot_service = DiscordBotService(bot_token)
            # 디스코드 봇을 실행하여 메시지 가져오기
            await bot_service.run_bot(num_messages)
            # ContentDB에서 메시지 필터링 및 정렬 후 리스트로 변환
            messages = await sync_to_async(list)(
                ContentDB.objects.filter(platform='discord').order_by('-id')[:num_messages].values('userID', 'userIcon', 'text', 'image_url')
            )
            for message in messages:
                # 프로필 이미지가 없을 경우 기본 이미지 설정
                if not message['userIcon']:
                    message['userIcon'] = DiscordBotView.DEFAULT_PROFILE_IMAGE_URL
                # 이미지 URL이 있는 경우 파일 데이터베이스에서 URL 가져오기
                if message['image_url'] != 0:
                    try:
                        file_db = await sync_to_async(FileDB.objects.get)(uid=message['image_url'])
                        message['image_url'] = file_db.url
                    except FileDB.DoesNotExist:
                        # 이미지가 존재하지 않으면 None 설정
                        message['image_url'] = None
                else:
                    message['image_url'] = None  # 이미지가 없는 경우 None 설정

            # 메시지 리스트를 JSON 형태로 반환
            return JsonResponse({'messages': messages})
        return JsonResponse({'error': 'Invalid request method'}, status=400)

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
    def set_token(request):
        """
        디스코드 봇 토큰을 설정하는 함수
        - POST 요청을 받아 토큰을 세션에 저장
        - GET 요청으로 토큰 설정 페이지를 렌더링
        """
        if request.method == 'POST':
            form = TokenForm(request.POST)
            if form.is_valid():
                # 유효한 폼 데이터를 세션에 저장
                request.session['bot_token'] = form.cleaned_data['bot_token']
                return redirect('index')
        else:
            form = TokenForm()
        # 토큰 설정 페이지를 렌더링
        return render(request, 'discord_template/set_token.html', {'form': form})
