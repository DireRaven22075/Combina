import json
import os
import ssl
import django
import sys
import discord
import warnings
import aiohttp
import base64
import requests
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
    def __init__(self, token, channel_id, intents=None):
        self.token = token
        self.channel_id = channel_id
        self.intents = intents or discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.client = discord.Client(intents=self.intents)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE  # SSL 검증 비활성화
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context))

    class MyClient(discord.Client):
        def __init__(self, token, num_messages, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.token = token
            self.num_messages = int(num_messages)

        async def setup_hook(self):
            self.loop.create_task(self.fetch_messages())

        async def fetch_messages(self):
            await self.wait_until_ready()

            channel_id_obj = await sync_to_async(DiscordChannel.objects.filter(platform='Discord').first)()
            if not channel_id_obj or not channel_id_obj.tag:
                print("Error: No channel ID found in the database or channel ID is empty.")
                return
            
            channelID = channel_id_obj.tag
            if not channelID.isdigit():
                print(f"Error: Channel ID is not valid: {channelID}")
                return

            print(f"Using Channel ID: {channelID}")  # 디버깅 로그 추가

            try:
                channel = self.get_channel(int(channelID))
                if not channel or not isinstance(channel, discord.TextChannel):
                    print(f"Error: Channel with ID {channelID} not found or is not a text channel.")
                    return

                await sync_to_async(DiscordMessage.objects.all().delete)()
                messages = [message async for message in channel.history(limit=self.num_messages)]
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
                        userID=username,
                        userIcon=profile_image_url,
                        text=message.content,
                        image_url=image_uid,
                        vote=0
                    )
            except Exception as e:
                print(f"Error fetching messages: {e}")
            finally:
                await self.close()

    async def run_bot(self, num_messages):
        timeout = aiohttp.ClientTimeout(total=60)  # 타임아웃 설정
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE  # SSL 검증 비활성화

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context), timeout=timeout) as session:
            client = self.MyClient(self.token, num_messages, intents=self.intents)
            try:
                await client.start(self.token)
                await client.wait_until_ready()
                channel = client.get_channel(int(self.channel_id))
                if channel is None:
                    print(f"Channel with ID {self.channel_id} not found.")
                    return None

                print(f"Channel {channel.name} found, fetching messages...")
                messages = [message async for message in channel.history(limit=num_messages)]
                if not messages:
                    print("No messages found in the channel.")
                    return None

                print(f"Retrieved {len(messages)} messages.")
                return messages
            except discord.errors.Forbidden as e:
                print(f"Bot does not have permission to access the channel: {e}")
                return None
            except Exception as e:
                print(f"Error running bot: {e}")
                return None
            finally:
                await client.close()
            
    async def send_message_to_discord(self, message, file_data=None, filename='image.png'):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
            try:
                url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"
                headers = {
                    "Authorization": f"Bot {self.token}"
                }

                form_data = aiohttp.FormData()
                form_data.add_field('payload_json', json.dumps({"content": message}), content_type='application/json')
                
                if file_data:
                    file_bytes = BytesIO(base64.b64decode(file_data))  # 파일 데이터를 BytesIO 객체로 변환
                    form_data.add_field('file', file_bytes, filename=filename, content_type='application/octet-stream')

                async with session.post(url, headers=headers, data=form_data) as response:
                    if response.status == 200:
                        print("Message sent successfully.")
                        return True
                    else:
                        print(f"Error sending message: {response.status}, {await response.text()}")
                        return False

            except Exception as e:
                print(f"Error sending message: {e}")
                return False

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
                    print(await response.text())
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
