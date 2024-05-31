from django.urls import path
from . import views
from asgiref.sync import async_to_sync

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-discord-messages/', async_to_sync(views.fetch_discord_messages), name='fetch_discord_messages'),
    path('send-discord-message/', async_to_sync(views.send_discord_message), name='send_discord_message'),
    path('set-channel-id/', async_to_sync(views.set_channel_id), name='set_channel_id'),
    path('update-bot-profile/', async_to_sync(views.update_bot_profile), name='update_bot_profile'),
]
