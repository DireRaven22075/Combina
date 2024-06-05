from . import views
from django.urls import include, path
from .views import *

urlpatterns = [
    path('home/', views.home, name="home"),
   
]