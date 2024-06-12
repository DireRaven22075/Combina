from . import views
from django.urls import path
from .views import Everytime
from asgiref.sync import async_to_sync

# 에브리타임은 크롤링을 연속적으로 하게 되면, 쿠키에 기록이 남고 로그인을 막음
# 환경이 바뀌었을 때 얼마까지 되는지는 모르겠음.
# driver의 설정은 account.py에 있음 account.py의 64번째 줄 쿠키 일일일 지우려고 길게함. 새 환경에서는 줄여도 괜찮을 거임
# post.py의 79,80 번째줄은 업로드 하고 싶을 때 주석 해제하면 됨.

urlpatterns = [
    path('connect/', Everytime.login_page, name='login'), #로그인 페이지 랜더링
    path('connect_info/', Everytime.ev_login, name='login_info'), #로그인 정보 받아서 처리
    path('get-content/', async_to_sync(Everytime.ev_free_field), name='free_field'), #에타 크롤링
    path('redirect_page/', Everytime.redirect_page, name="redirect_page"), #로그인 성공시 페이지 이동
    path('post/', async_to_sync(Everytime.ev_post), name='post'), #게시글 작성
    path('disconnect/', Everytime.logout, name='logout'), #에브리타임 로그아웃
    
    
    path('', Everytime.home, name='home'), #에브리타임 홈
   
]