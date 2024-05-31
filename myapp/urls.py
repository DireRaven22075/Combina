from django.urls import path
from asgiref.sync import async_to_sync
from .views import DiscordView

urlpatterns = [
    path('', DiscordView.index, name='index'),
    path('fetch-discord-messages/', async_to_sync(DiscordView.fetch_discord_messages), name='fetch_discord_messages'),
    path('send-discord-message/', async_to_sync(DiscordView.send_discord_message), name='send_discord_message'),
    path('set-channel-id/', async_to_sync(DiscordView.set_channel_id), name='set_channel_id'),
    path('update-bot-profile/', async_to_sync(DiscordView.update_bot_profile), name='update_bot_profile'),
]
