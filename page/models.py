from django.db import models

class AccountDB(models.Model):
    platform = models.CharField(max_length=30)
    token = models.TextField()
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=30)  # 채널 ID로 사용
    connected = models.BooleanField(default=False, null=False)

class ContentDB(models.Model):
    platform = models.CharField(max_length=30)
    time = models.DateTimeField()
    name = models.CharField(max_length=100, null=True)
    text = models.TextField()
    file = models.IntegerField()
    author_id = models.BigIntegerField(null=True)  # DiscordMessage의 author_id 추가
    image_url = models.URLField(blank=True, null=True)  # DiscordMessage의 image_url 추가
    profile_image_url = models.URLField(blank=True, null=True)  # DiscordMessage의 profile_image_url 추가

class FileDB(models.Model):
    uid = models.IntegerField()
    path = models.FilePathField()
    file = models.FileField()

class ChatDB(models.Model):
    owner = models.IntegerField()
    text = models.TextField()
    time = models.DateTimeField()
