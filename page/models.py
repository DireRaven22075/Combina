from django.db import models

class AccountDB(models.Model):
    platform = models.CharField(max_length=30)  # 해당 계정의 플랫폼 이름
    token = models.TextField()  # 해당 계정의 토큰
    name = models.CharField(max_length=100)  # 해당 계정의 이름
    tag = models.CharField(max_length=30)  # 미사용 (Discord only)
    connected = models.BooleanField(default=False, null=False)  # 연결 여부
    icon = models.URLField()  # 해당 계정의 아이콘

class ContentDB(models.Model):
    platform = models.CharField(max_length=30)  # Discord == discord // Discord
    userID = models.CharField(max_length=100, default='default_userID')  # Discord : user_id // Everytime: username
    text = models.TextField()  # Discord : content // Everytime: title + text
    image_url = models.BigIntegerField(default=0)  # 숫자형 기본 값 설정
    userIcon = models.URLField(default='http://default.url/icon.png')  # URL 기본 값 설정
    vote = models.BigIntegerField(default=0)  # 숫자형 기본 값 설정
    url = models.URLField(default='http://default.url/icon.png')  # URL 기본 값 설정

class FileDB(models.Model):
    uid = models.IntegerField(null=False)
    url = models.URLField(default='http://default.url/icon.png')  # URL 기본 값 설정

class Setting(models.Model):
    theme = models.CharField(max_length=30, default='light')  # 테마 설정
    redditSize = models.IntegerField(default=10, null=False)  # 레딧 컨텐츠 불러오는 개수
    youtubeSize = models.IntegerField(default=10, null=False)  # 유튜브 컨텐츠 불러오는 개수
    everytimeSize = models.IntegerField(default=10, null=False)  # 에브리타임 컨텐츠 불러오는 개수
    url = models.URLField(default='http://default.url/icon.png')  # URL 기본 값 설정