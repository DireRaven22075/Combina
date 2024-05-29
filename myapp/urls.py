from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-discord-messages/', views.fetch_discord_messages, name='fetch_discord_messages'),
    path('send-discord-message/', views.send_discord_message, name='send_discord_message'),
    path('set-channel-id/', views.set_channel_id, name='set_channel_id'),
]
