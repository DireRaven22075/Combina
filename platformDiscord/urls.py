from django.urls import path
from .views import DiscordBotView
from asgiref.sync import async_to_sync

urlpatterns = [
    path('', DiscordBotView.index, name='index'), # 메인 페이지 URL
    path('fetch-discord-messages/', async_to_sync(DiscordBotView.fetch_discord_messages), name='fetch_discord_messages'), # 디스코드 메세지 가져오기
    path('send-discord-message/', async_to_sync(DiscordBotView.send_discord_message), name='send_discord_message'), # 디스코드 메시지 보내기
    path('set-channel-id/', async_to_sync(DiscordBotView.set_channel_id), name='set_channel_id'), # 디스코드 채널 ID 설정
    path('update-bot-profile/', async_to_sync(DiscordBotView.update_bot_profile_view), name='update_bot_profile'), # 디스코드 봇 프로필 업데이트
    path('set-token/', DiscordBotView.set_token, name='set_token'), # 디스코드 봇 토큰 설정
]
