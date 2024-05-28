from typing import Any
from django.shortcuts import render, redirect
from tweety import Twitter
from .models import Account, Content
from django.contrib import messages
from django.views import View



import os
current_directory = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(current_directory, '../password.txt'))
f = open(path)
email = f.readline()
password = f.readline()
app = Twitter("session")
print(app.sign_in(email, password))



def home(request):
    return render(request, 'template/page/home.html')

def login(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        app = Twitter("session")
        is_user = app.sign_in(email, password)
        if is_user != None:
            messages.success(request, '로그인 성공')
            user = Account.objects.create(email=email, password=password, connect=1)
            user.save()
            return redirect('/')
        else:
            messages.error(request, '로그인 실패')
    return render(request, 'template/page/login.html')


def search_tweet(request):
    if request.method == 'POST':
        print(request.POST)
        search = request.POST.get('search')
        search_tweet = app.search(keyword=search, pages=1)[:5]
        tweets = []
        for tweet in search_tweet:
            tweet_detail = app.tweet_detail(tweet['id'])
            if tweet_detail is not None:
                tweets.append({
                    'tweet_name': tweet_detail.author.name,
                    'tweet_username': tweet_detail.author.username,
                    'tweet_text': tweet_detail.text.split('https')[0],
                    'tweet_date': tweet_detail.date
                })
                print(tweet)
        context = {
            'tweets': tweets
        }
        return render(request, 'template/page/home.html', context)
    return redirect('/')

