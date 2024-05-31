from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DiscordMessage, DiscordChannel

admin.site.register(DiscordMessage)
admin.site.register(DiscordChannel)