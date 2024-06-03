from django.contrib import admin
from .models import Account, Content
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'email', 'created_at', 'tag', 'color')
    list_filter = ('platform', 'created_at', 'tag', 'color')
    search_fields = ('name', 'email')

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('Account', 'name', 'platform', 'text', 'date', 'icon')

    search_fields = ('Account', 'name', 'platform', 'text', 'date', 'icon')
