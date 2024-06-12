from django.urls import path
from .views import DiscordBotView, RedirectPageView, PostAccountView, DisconnectView
from asgiref.sync import async_to_sync

app_name = 'platformDiscord'

urlpatterns = [
    path('', DiscordBotView.index, name='index'),
    path('get-content/', async_to_sync(DiscordBotView.get_content), name='get_content'),
    path('send-discord-message/', async_to_sync(DiscordBotView.send_discord_message), name='send_discord_message'),
    path('set-channel-id/', async_to_sync(DiscordBotView.set_channel_id), name='set_channel_id'),
    path('update-bot-profile/', async_to_sync(DiscordBotView.update_bot_profile_view), name='update_bot_profile'),
    path('connect/', DiscordBotView.connect, name='connect'),
    path('redirect-page/', RedirectPageView.as_view(), name='redirect_page'),
    path('post-account/', PostAccountView.as_view(), name='post_account'),
    path('disconnect/', DisconnectView.as_view(), name='disconnect'),
]