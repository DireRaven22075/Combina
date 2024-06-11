from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('info/', views.login_info, name='login'),
    #path('logout/', views.logout, name='logout'),

    # Add more URL patterns here
]