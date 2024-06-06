from django.db import models

class AccountDB(models.Model):
    platform = models.CharField(max_length=30)
    token = models.TextField()
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=30)  # 채널 ID로 사용
    connected = models.BooleanField(default=False, null=False)

class ContentDB(models.Model):
    platform = models.CharField(max_length=30)  # Discord == discord // Discord
    userID = models.CharField(max_length=100, default='default_userID')  # Discord : user_id // Everytime: username
    text = models.TextField()  # Discord : content // Everytime: title + text
    image_url = models.BigIntegerField(default=0)  # 숫자형 기본 값 설정
    userIcon = models.URLField(default='http://default.url/icon.png')  # URL 기본 값 설정
    vote = models.BigIntegerField(default=0)  # 숫자형 기본 값 설정

class FileDB(models.Model):
    uid = models.IntegerField(null=False)
    url = models.URLField(default='http://default.url/icon.png')  # URL 기본 값 설정
