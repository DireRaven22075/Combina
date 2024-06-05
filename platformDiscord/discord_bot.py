import os
import django
import sys
import discord
import warnings
import aiohttp
import base64
from asgiref.sync import sync_to_async
from io import BytesIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'combina.settings')

django.setup()

from page.models import ContentDB as DiscordMessage, AccountDB as DiscordChannel

warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<TCPTransport.*>")

class DiscordBotService:
    def __init__(self, token):
        self.token = token
        self.intents = discord.Intents.default()
        self.intents.message_content = True

    class MyClient(discord.Client):
        def __init__(self, token, num_messages, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.token = token
            self.num_messages = int(num_messages)

        async def setup_hook(self):
            self.loop.create_task(self.fetch_messages())

        async def fetch_messages(self):
            await self.wait_until_ready()
            channel_id_obj = await sync_to_async(DiscordChannel.objects.first)()
            if channel_id_obj:
                channelID = channel_id_obj.tag  # tag 필드를 사용
            else:
                print("Error: No channel ID found in the database.")
                return

            channel = self.get_channel(int(channelID))  # 채널 ID가 정수일 경우 변환
            if not channel or not isinstance(channel, discord.TextChannel):
                print(f"Error: Channel with ID {channelID} not found or is not a text channel.")
                return

            await sync_to_async(DiscordMessage.objects.all().delete)()
            messages = [message async for message in channel.history(limit=self.num_messages)]
            for message in messages:
                image_url = None
                if message.attachments:
                    image_url = message.attachments[0].url  # 첫 번째 첨부 파일의 URL 가져오기
                profile_image_url = str(message.author.avatar.url) if message.author.avatar else None  # 프로필 이미지 URL 가져오기
                await sync_to_async(DiscordMessage.objects.create)(
                    text=message.content,  # content를 text로 저장
                    name=message.author.name,  # author를 name으로 저장
                    author_id=message.author.id,  # 사용자 ID 저장
                    image_url=image_url,
                    profile_image_url=profile_image_url,  # 프로필 이미지 URL 저장
                    platform='discord',  # 플랫폼 지정
                    time=message.created_at,  # 메시지 생성 시간
                    file=0  # 기본 파일 ID 설정 (필요시 수정)
                )
            await self.close()


    async def run_bot(self, num_messages):
        client = self.MyClient(self.token, num_messages, intents=self.intents)
        try:
            await client.start(self.token)
        except Exception as e:
            print(f"Error running bot: {e}")
        finally:
            await client.close()

    async def send_message_to_discord(self, message, image_data=None):
        client = self.MyClient(self.token, 20, intents=self.intents)  # 기본 메시지 수 20개로 설정
        try:
            await client.login(self.token)
            await client.connect()

            channel_id_obj = await sync_to_async(DiscordChannel.objects.first)()
            if channel_id_obj:
                channelID = channel_id_obj.tag  # tag 필드를 사용
            else:
                print("Error: No channel ID found in the database.")
                return False

            channel = client.get_channel(int(channelID))  # 채널 ID가 정수일 경우 변환
            if channel and isinstance(channel, discord.TextChannel):
                if image_data:
                    image = BytesIO(base64.b64decode(image_data))
                    await channel.send(message, file=discord.File(image, filename="image.png"))
                else:
                    await channel.send(message)
                return True
            return False
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
        finally:
            try:
                await client.close()
            except Exception as e:
                print(f"Error closing client: {e}")

    async def update_bot_profile(self, bot_name=None, bot_avatar=None):
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
                    print("Bot profile updated successfully.")
                    return True
                else:
                    print(f"Error updating bot profile: {response.status}")
                    print(await response.text())  # 오류 메시지 확인
                    return False
