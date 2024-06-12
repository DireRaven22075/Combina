import os
import django
import sys
import discord
import warnings
import aiohttp
import base64
import requests  # requests 모듈 임포트
from django.db import models
from asgiref.sync import sync_to_async
from page.models import ContentDB as DiscordMessage, AccountDB as DiscordChannel, FileDB
from io import BytesIO

# Django 환경 설정을 위한 초기화
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'combina.settings')
django.setup()

# TCPTransport 경고 무시
warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<TCPTransport.*>")

class DiscordBotService:
    """
    디스코드 봇의 주요 기능을 담당하는 클래스.
    토큰을 통해 봇을 초기화하고 메시지 전송 및 가져오기, 프로필 업데이트 등을 수행.
    """

    def __init__(self, token):
        """
        디스코드 봇의 토큰을 초기화하고, 필요한 권한을 설정.
        :param token: 디스코드 봇의 인증 토큰
        """
        self.token = token
        self.intents = discord.Intents.default()
        self.intents.message_content = True  # 메시지 내용을 읽기 위한 권한
        self.intents.members = True  # 멤버 정보를 읽기 위한 권한
        self.client = discord.Client(intents=self.intents)  # intents 인자를 추가

    class MyClient(discord.Client):
        """
        디스코드 클라이언트를 상속받아 메시지 가져오기 등의 작업을 처리하는 클래스.
        """

        def __init__(self, token, num_messages, *args, **kwargs):
            """
            클라이언트 초기화.
            :param token: 디스코드 봇의 인증 토큰
            :param num_messages: 가져올 메시지의 개수
            """
            super().__init__(*args, **kwargs)
            self.token = token
            self.num_messages = int(num_messages)

        async def setup_hook(self):
            """
            클라이언트가 준비된 후 메시지 가져오기 작업을 예약.
            """
            self.loop.create_task(self.fetch_messages())

        async def fetch_messages(self):
            """
            디스코드 채널에서 메시지를 가져와서 데이터베이스에 저장.
            """
            await self.wait_until_ready()  # 클라이언트가 준비될 때까지 대기
            channel_id_obj = await sync_to_async(DiscordChannel.objects.first)()  # 첫 번째 채널 ID 가져오기
            if channel_id_obj:
                channelID = channel_id_obj.tag
            else:
                print("Error: No channel ID found in the database.")
                return

            channel = self.get_channel(int(channelID))  # 채널 ID로 채널 가져오기
            if not channel or not isinstance(channel, discord.TextChannel):
                print(f"Error: Channel with ID {channelID} not found or is not a text channel.")
                return

            await sync_to_async(DiscordMessage.objects.all().delete)()  # 기존 메시지 삭제
            messages = [message async for message in channel.history(limit=self.num_messages)]  # 메시지 가져오기
            for message in messages:
                image_uid = 0
                if message.attachments:
                    file_url = message.attachments[0].url
                    max_uid = await sync_to_async(lambda: FileDB.objects.aggregate(models.Max('uid'))['uid__max'] or 0)()
                    new_uid = max_uid + 1 if max_uid is not None else 1
                    file_db = await sync_to_async(FileDB.objects.create)(uid=new_uid, url=file_url)
                    image_uid = file_db.uid

                profile_image_url = str(message.author.display_avatar.url) if message.author.display_avatar else 'http://default.url/icon.png'
                username = message.author.name
                await sync_to_async(DiscordMessage.objects.create)(
                    platform='discord',
                    userID=username,  # userID 필드에 사용자 이름을 저장
                    userIcon=profile_image_url,
                    text=message.content,
                    image_url=image_uid,
                    vote=0
                )
            await self.close()  # 메시지 가져온 후 클라이언트 종료

    async def run_bot(self, num_messages):
        """
        디스코드 봇을 시작하고, 지정된 개수만큼의 메시지를 가져옴.
        :param num_messages: 가져올 메시지의 개수
        """
        client = self.MyClient(self.token, num_messages, intents=self.intents)
        try:
            await client.start(self.token)  # 봇 시작
        except Exception as e:
            print(f"Error running bot: {e}")  # 예외 발생 시 출력
        finally:
            await client.close()  # 클라이언트 종료

    async def send_message_to_discord(self, message, image_data=None):
        """
        메시지와 이미지를 디스코드 채널로 전송.
        :param message: 전송할 메시지 내용
        :param image_data: 전송할 이미지 데이터 (Base64 인코딩)
        :return: 성공 여부
        """
        client = self.MyClient(self.token, 20, intents=self.intents)  # intents 인자를 추가
        try:
            await client.login(self.token)  # 봇 로그인
            await client.connect()  # 봇 연결

            channel_id_obj = await sync_to_async(DiscordChannel.objects.first)()  # 첫 번째 채널 ID 가져오기
            if channel_id_obj:
                channelID = channel_id_obj.tag  # tag 필드를 사용
            else:
                print("Error: No channel ID found in the database.")
                return False

            channel = client.get_channel(int(channelID))  # 채널 ID가 정수일 경우 변환
            if channel and isinstance(channel, discord.TextChannel):
                if image_data:
                    image = BytesIO(base64.b64decode(image_data))
                    await channel.send(message, file=discord.File(image, filename="image.png"))  # 이미지와 메시지 전송
                else:
                    await channel.send(message)  # 메시지 전송
                return True
            return False
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
        finally:
            try:
                await client.close()  # 클라이언트 종료
            except Exception as e:
                print(f"Error closing client: {e}")

    async def update_bot_profile(self, bot_name=None, bot_avatar=None):
        """
        디스코드 봇의 프로필을 업데이트.
        :param bot_name: 새 봇 이름
        :param bot_avatar: 새 봇 아바타 (Base64 인코딩)
        :return: 성공 여부
        """
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bot {self.token}',
                'Content-Type': 'application/json'
            }
            json_data = {}
            if bot_name:
                json_data['username'] = bot_name
            if bot_avatar:
                json_data['avatar'] = bot_avatar

            async with session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=json_data) as response:
                if response.status == 200:
                    print("Bot profile updated successfully.")  # 성공 메시지 출력
                    return True
                else:
                    print(f"Error updating bot profile: {response.status}")
                    print(await response.text())  # 오류 메시지 확인
                    return False

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
