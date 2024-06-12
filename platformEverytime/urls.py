from . import views
from django.urls import path
from .views import Everytime
from asgiref.sync import async_to_sync

# POST["page"] 값 init 인지 account인지 구별 및 처리

urlpatterns = [
    path('', Everytime.home, name='home'),
    path('connect/', Everytime.login_page, name='login'), #로그인 페이지 랜더링
    path('connect_info/', Everytime.ev_login, name='login_info'), #로그인 처리
    path('get-content/', async_to_sync(Everytime.ev_free_field), name='free_field'),
    path('redirect_page/', Everytime.redirect_page, name="redirect_page"),
    path('post/', async_to_sync(Everytime.ev_post), name='post'),
    path('post_field/', async_to_sync(Everytime.ev_post), name='post_field'),
    path('disconnect/', Everytime.logout, name='logout'), #logout
    #path('search/', async_to_sync(Everytime.ev_search_field), name='search_field'),
    #path('connect', )
]