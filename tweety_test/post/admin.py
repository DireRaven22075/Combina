from django.contrib import admin
from .forms import TweetForm
from .models import Post
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    form = TweetForm
    list_display = ('text','image')
    list_filter = ('text', 'image')
    search_fields = ('text',)

admin.site.register(Post, TweetAdmin)