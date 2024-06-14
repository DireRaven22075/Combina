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
    async def GetContent(request):
        account = AccountDB.objects.filter(platform='Discord').first()
        bot_token = account.token
        channel_id = account.tag
        bot_service = DiscordBotService(bot_token, channel_id, discord.Intents.default())
        num_messages = 20
        messages = await bot_service.run_bot(num_messages)
        data = []
        for message in messages:
            data.append({
                'userID': message.author.name,
                'userIcon': str(message.author.display_avatar.url) if message.author.display_avatar else 'http://default.url/icon.png',
                'text': message.content,
                'image_url': message.attachments[0].url if message.attachments else None
            })
        
        return JsonResponse({'messages': data})

    @csrf_exempt
    async def get_content(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                num_messages = int(data.get('num_messages', 20))
                account = await sync_to_async(AccountDB.objects.filter(platform='Discord').first)()
                if not account or not account.token:
                    return JsonResponse({'error': 'Bot token not found in database'}, status=400)

                bot_token = account.token
                channel_id = account.tag
                bot_service = DiscordBotService(bot_token, channel_id)
                messages = await bot_service.fetch_messages(num_messages)

                if messages is None:
                    return JsonResponse({'error': 'No messages retrieved from Discord API'}, status=500)

                response_data = [
                    {
                        'userID': msg['author']['username'],
                        'userIcon': msg['author']['avatar'],
                        'text': msg['content'],
                        'image_url': msg['attachments'][0]['url'] if msg['attachments'] else None
                    } for msg in messages
                ]

                return JsonResponse({'messages': response_data})
            except Exception as e:
                print(f"Error in get_content: {e}")
                return JsonResponse({'error': str(e)}, status=500)
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

    @csrf_exempt
    async def send_discord_message(request):
        """
        TODO: 이미지 전송 에러 수정 필요
        
        시도 내역:
        1. 이미지 데이터를 Base64로 인코딩하여 전송 (실패)
            - 이유: Discord API가 Base64 데이터를 지원하지 않음
        2. 이미지 데이터를 BytesIO로 변환하여 전송 (실패)
            - 이유: 데이터 변환 후 Discord API와의 호환성 문제
        3. 이미지 데이터를 BytesIO로 변환 후 Base64로 인코딩하여 전송 (실패)
            - 이유: 데이터 크기 증가로 인한 전송 문제
        4. 이미지 파일을 직접 Discord API로 전송 (실패)
            - 이유: 이미지 파일 전송 시도 실패
        5. SSL 에러 발생 시 예외 처리 (실패)
            - 이유: SSL 오류가 반복적으로 발생, 원인 불명
        6. 별도의 이미지 전송 함수를 만들어 이미지 전송 (실패)
            - 이유: 동일한 이미지 전송 실패 문제 지속
        7. 이미지 파일 별도 저장 후 전송 (실패)
            - 이유: 파일 경로 문제로 인해 전송 실패
        8. 이미지 URL을 전송하여 이미지 전송 (실패)
            - 이유: URL 형식 불일치 혹은 접근 권한 문제
        9. send_message_to_discord 전체 함수 갈아엎고 새로 작성 (실패)
            - 이유: 기존 문제 해결 불가, 근본적인 원인 불명
        10. 서버 응답 처리 및 재시도 로직 추가 (실패)
            - 이유: 응답 처리 로직 추가에도 동일한 전송 실패 문제 발생
        11. 타임아웃 및 연결 설정 변경 (실패)
            - 이유: 타임아웃 연장에도 동일한 SSL 오류 발생
        12. 이미지 전송 함수를 별도로 분리 (실패)
            - 이유: 이미지 전송 함수 자체의 문제 해결되지 않음
        13. 이미지 전송 함수에 예외 처리 추가 (실패)
            - 이유: 예외 처리에도 불구하고 기본적인 전송 문제 지속
        14. 이미지 전송 함수에 디버깅 코드 추가 (실패)
            - 이유: 디버깅 코드로도 정확한 원인 파악 불가
        15. 네트워크 연결 상태 및 방화벽 설정 확인 (이상 없음)
        16. 서버 및 클라이언트의 최신 상태 유지 (이상 없음)
        17. Discord API 문서 및 커뮤니티 리소스 참고 (이상 없음)
        18. 기타 구글링 및 스택오버플로우 검색 (수확 없음)
        19. copilot의 제안을 참고하여 코드 수정 (실패)
        20. GPT 사용 (GPT-4도 문제 해결 불가)

        추가 시도 필요:
        - 파일 전송 방식 변경 (예: multipart/form-data 활용)
        - 이미지 파일 크기를 줄이거나 다른 형식으로 변환 시도
        - 관련된 외부 라이브러리, 플러그인 활용
            - 예: `discord.py` 라이브러리의 `send_file` 메서드 사용
        - 네트워크 트래픽 분석 도구 사용 (예: Wireshark)
        - Discord API 지원팀에 문의하여 자세한 가이드 요청
    """
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                title = data.get('title', 'No Title')
                text = data.get('text', '')
                files = data.get('files', [])

                account = await sync_to_async(AccountDB.objects.filter(platform='Discord').first)()
                if not account or not account.token:
                    return JsonResponse({'error': 'Bot token not found in database'}, status=400)
                bot_token = account.token

                bot_service = DiscordBotService(bot_token, account.tag, discord.Intents.default())
                message_content = f"**{title}**\n\n{text}"

                if files:
                    file_data = files[0]['data']
                    filename = files[0]['name']
                    await bot_service.send_message_to_discord(message_content, file_data, filename)
                else:
                    await bot_service.send_message_to_discord(message_content)

                return JsonResponse({'success': True})
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON format')
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': 'Invalid request method'})

    
    @staticmethod
    @csrf_exempt
    async def set_channel_id(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            channel_id_str = data.get('channel_id', '')
            print(f"Received Channel ID: '{channel_id_str}'")  # 디버깅 로그 추가

            if not channel_id_str:
                return JsonResponse({'error': 'No channel ID provided'}, status=400)
            if not channel_id_str.isdigit():
                return JsonResponse({'error': 'Invalid channel ID format. It must be a numerical value.'}, status=400)

            channel_id = int(channel_id_str)
            account, created = await sync_to_async(AccountDB.objects.get_or_create)(platform='Discord')
            account.tag = channel_id
            await sync_to_async(account.save)()
            print(f"Channel ID {channel_id} set for Discord account.")

            return JsonResponse({'success': True, 'channel_id': channel_id})
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

                    # get_or_create 반환 값을 두 개의 변수로 나눔
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
    def Disconnect(request):
        discord_account = AccountDB.objects.filter(platform='Discord').first()
        discord_account.name = ""
        discord_account.tag = ""
        discord_account.token = ""
        discord_account.connected = False
        discord_account.save()
        return redirect(request.META.get('HTTP_REFERER', '/accounts'))

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
