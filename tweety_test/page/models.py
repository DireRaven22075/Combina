from django.db import models
import json
from django.contrib.postgres.fields import ArrayField
#from django.db.models import JSONField#이것도 인식 못함

#from django.contrib.postgres.fields import JSONField #sqlite 가 인식 못한다 ㅠㅠ
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
    Account = models.ForeignKey('Account',null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="None")
    platform = models.CharField(max_length=20, null=True)
    text = models.TextField()
    images = models.JSONField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    icon = models.ImageField(upload_to='images/', null=True, blank=True)
    tag = models.CharField(max_length=20, default='None')
    def __list__(self):
        self.contents = [self.name, self.platform, self.text, self.date, self.icon, self.tag]
        return self.contents
    
    def to_json(self):
        return json.dumps({
            'account': self.Account,
            'name': self.name,
            'platform': self.platform,
            'text': self.text,
            'date': self.date.isoformat(),
            'icon': self.icon.url if self.icon else None,
            #'images': Image.objects.filter(content=self).values_list('image', flat=True),
            'tag': self.tag,
        })
    
# class Image(models.Model):
#     content = models.ForeignKey('Content', related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/', null=True, blank=True)

# class ContentImage(models.Model):
#     content = models.ForeignKey('Content', related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images/')

#     def __str__(self):
#         return f"Image for {self.content.name}"
