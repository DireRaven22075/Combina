from django.urls import path
from .views import DiscordView

urlpatterns = [
    path('', DiscordView.index, name='index'),
    path('fetch-discord-messages/', DiscordView.fetch_discord_messages, name='fetch_discord_messages'),
    path('send-discord-message/', DiscordView.send_discord_message, name='send_discord_message'),
    path('set-channel-id/', DiscordView.set_channel_id, name='set_channel_id'),
]
