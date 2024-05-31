from django.urls import path
from .views import *
from .sql import *
from asgiref.sync import async_to_sync
urlpatterns = [
    path('', Home, name='home'),
    path('home/', Home, name='home'),
    path('find/', Find, name='find'),
    path('post/', Post, name='post'),
    path('chat/', Chat, name='chat'),
    path('chat/<str:platform>/<int:id>/', InChat, name='inchat'),
    path('menu/', Menu, name='menu'),
    path('server/post', Server.Post),
    path('server/disconnect', Disconnect, name='disconnect'),
    path('temp/test', DBTest, name='temp'),
    #discord
    path('discord/', DiscordView.index, name='index'),
    path('fetch-discord-messages/', async_to_sync(DiscordView.fetch_discord_messages), name='fetch_discord_messages'),
    path('send-discord-message/', async_to_sync(DiscordView.send_discord_message), name='send_discord_message'),
    path('set-channel-id/', async_to_sync(DiscordView.set_channel_id), name='set_channel_id'),
    path('update-bot-profile/', async_to_sync(DiscordView.update_bot_profile), name='update_bot_profile'),
]