from . import views
from django.urls import include, path

from pathlib import Path


urlpatterns = [
    path('', include('platformEverytime.search.urls')),
    path('account/', include('platformEverytime.account.urls')),
    path('post/', include('platformEverytime.post.urls')),
]