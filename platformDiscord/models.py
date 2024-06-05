#platformDiscord/models.py
from django.db import models

class DiscordMessage(models.Model):
    author = models.CharField(max_length=100)
    author_id = models.BigIntegerField(null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.author}: {self.content}'

class DiscordChannel(models.Model):
    channel_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.channel_id)