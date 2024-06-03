from django.db import models
from page.models import Account, Content
import json


# # Create your models here.
# def tweet_image_path(instance, filename):
#     return f'tweet/{instance.pk}/images/{filename}'




class Post(Content):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    def __str__(self):
        return self.text
    
    
