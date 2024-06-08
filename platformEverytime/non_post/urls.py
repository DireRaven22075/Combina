from . import views
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', views.post, name="first page to post"),
    path('post_info/', views.post, name="post_info"),
]