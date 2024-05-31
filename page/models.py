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