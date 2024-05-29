from django.db import models

class DiscordMessage(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=255, default='Unknown')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content} at {self.timestamp}"

class DiscordChannel(models.Model):
    channel_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.channel_id)
