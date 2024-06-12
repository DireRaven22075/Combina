from . import views
from django.urls import path
from .views import Everytime
from asgiref.sync import async_to_sync

# POST["page"] 값 init 인지 account인지 구별 및 처리

urlpatterns = [
    path('connect/', Everytime.login_page, name='login'), #로그인 페이지 랜더링
    path('connect_info/', Everytime.ev_login, name='login_info'), #로그인 정보 받아서 처리
    path('get-content/', async_to_sync(Everytime.ev_free_field), name='free_field'), #에타 크롤링
    path('redirect_page/', Everytime.redirect_page, name="redirect_page"), #로그인 성공시 페이지 이동
    path('post/', async_to_sync(Everytime.ev_post), name='post'), #게시글 작성
    path('disconnect/', Everytime.logout, name='logout'), #에브리타임 로그아웃
    
    
    path('', Everytime.home, name='home'), #에브리타임 홈
   
]