from . import views
from django.urls import path
from .views import Everytime

urlpatterns = [
    path('', Everytime.home, name='home'),
    path('account/', Everytime.ev_login, name='login'),
    path('login_info/', Everytime.ev_login, name='login_info'),
    path('post/', Everytime.ev_post, name='post'),
    path('post_field/', Everytime.ev_post, name='post_field'),
    path('free_field/', Everytime.ev_free_field, name='free_field'),
    path('search/', Everytime.ev_search_field, name='search_field'),
]