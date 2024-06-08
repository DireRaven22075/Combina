from . import views
from django.urls import path
from .views import Everytime

urlpatterns = [
    path('', Everytime.home, name='home'),
    path('account/', Everytime.ev_login, name='login'),
    path('account/login_info/', Everytime.ev_login, name='login_info'),
    path('logout/', Everytime.ev_logout, name='logout'),
    path('post/', Everytime.ev_post, name='post'),
    path('free_field/', Everytime.ev_free_field, name='free_field'),
    path('search_field/', Everytime.ev_search_field, name='search_field'),
]