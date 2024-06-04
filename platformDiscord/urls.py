from django.urls import path
from .views import DiscordBotView
from asgiref.sync import async_to_sync

urlpatterns = [
    path('', DiscordBotView.index, name='index'),
    path('fetch-discord-messages/', async_to_sync(DiscordBotView.fetch_discord_messages), name='fetch_discord_messages'),
    path('send-discord-message/', async_to_sync(DiscordBotView.send_discord_message), name='send_discord_message'),
    path('set-channel-id/', async_to_sync(DiscordBotView.set_channel_id), name='set_channel_id'),
    path('update-bot-profile/', async_to_sync(DiscordBotView.update_bot_profile_view), name='update_bot_profile'),
    path('set-token/', DiscordBotView.set_token, name='set_token'),
]
