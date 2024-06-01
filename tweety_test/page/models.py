from django.db import models

# Create your models here.

class Account(models.Model):
    connect = models.BooleanField(default=False)
    name = models.CharField(max_length=20, default="None")
    platform = models.CharField(max_length=20)
    email = models.CharField(max_length=20, default="None")
    password = models.CharField(max_length=20, default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=20, default='None')
    color = models.CharField(max_length=20, default='None')
    def __list__(self):
        self.accounts = [self.name, self.platform, self.email, self.password, self.created_at, self.tag, self.color]
        return self.accounts

class Content(models.Model):
    Account = models.ForeignKey('Account', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="None")
    platform = models.CharField(max_length=20)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='images/', default='None')
    image = models.ImageField(upload_to='images/', default='None')
    tag = models.CharField(max_length=20, default='None')
    def __list__(self):
        self.contents = [self.name, self.platform, self.text, self.date, self.icon, self.image, self.tag]
        return self.contents