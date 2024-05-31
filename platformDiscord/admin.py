from django.contrib import admin
from .models import DiscordMessage, DiscordChannel

admin.site.register(DiscordMessage)
admin.site.register(DiscordChannel)
