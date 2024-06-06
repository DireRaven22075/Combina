from . import views
from django.urls import include, path

from pathlib import Path


urlpatterns = [
    path('', include('everytime.search.urls')),
    #path('post/', include('everytime.post.urls')),
    #path('account/', include('everytime.account.urls')),
]