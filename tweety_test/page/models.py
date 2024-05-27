from django.db import models

# Create your models here.

class Account(models.Model):
    connect = models.IntegerField(default=0)
    name = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=20, default='none')
    color = models.CharField(max_length=20, default='none')
    def __list__(self):
        self.list = [self.name, self.platform, self.email, self.password, self.created_at, self.tag, self.color]
        return self.list

class Content(models.Model):
    name = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    text = models.TextField()
    date = models.DateTimeField(auto_now=False)
    icon = models.ImageField(upload_to='images/', default='none')
    image = models.ImageField(upload_to='images/', default='none')
    tag = models.CharField(max_length=20, default='none')
    def __list__(self):
        self.list = [self.name, self.platform, self.text, self.date, self.icon, self.image, self.tag]
        return self.list