from django.db import models

class AccountDB(models.Model):
    platform = models.CharField(max_length=30)
    token = models.TextField()
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=30)  # 채널 ID로 사용
    connected = models.BooleanField(default=False, null=False)

class ContentDB(models.Model):
    platform = models.CharField(max_length=30) #Discord == discord // Discord
    userID = models.CharField(max_length=100) #Discord : user_id // Everytime: username
    text = models.TextField() #Discord : content // Everytime: title + text
    image_url = models.BigIntegerField()
    userIcon = models.URLField()
    vote = models.BigIntegerField()

class FileDB(models.Model):
    uid = models.IntegerField()
    url = models.URLField()
# Modified 20240.06.05