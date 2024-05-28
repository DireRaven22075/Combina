from django.db import models
# Create your models here.
class AccountDB(models.Model):
    uid = models.AutoField(primary_key=True)
    connected = models.BooleanField(default=False, null=False)
    platform = models.CharField(max_length=30)
    id = models.CharField(max_length=100)
    name = models.TextField()
    tag = models.TextField()

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

class ChatDB(models.Model):
    target = models.CharField(max_length=30)
    time = models.DateTimeField()
    text = models.TextField()
    def __str__(self):
        return self.text