from django.urls import path
from . import views

urlpatterns = [
    path('', views.post, name='post'),
    path('info/', views.create_post, name='create_post'),
]
