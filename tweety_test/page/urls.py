from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage_index'),  # homepage 앱의 기본 페이지
    path('login/', views.login, name='login'),  # 로그인 페이지
    path('search/', views.search_tweet, name='search'),  # 검색 페이지
    path('login/info/', views.login, name='create user'),
]
