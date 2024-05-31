from django.db import models
# Create your models here.
class AccountDB(models.Model):
    platform = models.CharField(max_length=30)
    token = models.TextField()
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=30)
    connected = models.BooleanField(default=False, null=False)

class ContentDB(models.Model):
    platform = models.CharField(max_length=30)
    time = models.DateTimeField()
    name = models.CharField(max_length=100)
    text = models.TextField()
    file = models.IntegerField()

class FileDB(models.Model):
    uid = models.IntegerField()
    path = models.FilePathField()
    file = models.FileField()

class ChatDB(models.Model):
    owner = models.IntegerField()
    text = models.TextField()
    time = models.DateTimeField()



class ContentDB(models.Model):
    platform = models.CharField(max_length=30)
    account = models.CharField(max_length=100)
    time = models.DateTimeField()
    text = models.TextField()
    def __str__(self):
        return self.text

class ChatTableDB(models.Model):
    platform = models.CharField(max_length=30)
    account = models.CharField(max_length=100)
    time = models.DateTimeField()
    topMessage = models.TextField()
    topMessageTime = models.DateTimeField()
    chatdb = models.ForeignKey('ChatDB', on_delete=models.CASCADE)
    def __str__(self):
        return self.text
    
#discord

class DiscordMessage(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=255, default='Unknown')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'page'

    def __str__(self):
        return f"{self.author}: {self.content} at {self.timestamp}"

class DiscordChannel(models.Model):
    channel_id = models.BigIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'page'

    def __str__(self):
        return str(self.channel_id)