from django.contrib import admin
from .models import Account, Content
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'email', 'created_at', 'tag', 'color')
    list_filter = ('platform', 'created_at', 'tag', 'color')
    search_fields = ('name', 'email')

@admin.register(Content)
class ContentAdmin(admin.StackedInline):
    list_display = ('Account', 'content')
    search_fields = ('Account', 'content')