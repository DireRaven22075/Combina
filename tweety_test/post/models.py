from django.db import models
from page.models import Account, Content
import json

# Create your models here.

class Account(Account):
    pass

class Post(Content):
    post_image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    
