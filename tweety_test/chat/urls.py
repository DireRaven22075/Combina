from django.urls import path
from .import views

urlpatterns = [
    path('', views.chat, name='chat_index'),
    path('info/', views.chat_log, name='chat_log'),
]