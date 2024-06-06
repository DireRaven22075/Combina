from . import views
from django.urls import include, path
from .views import *

urlpatterns = [
    path('', views.login, name="login"),
    path('login_info/', views.login, name="login_info"),
    #path('logout/', views.logout, name="logout"),
]