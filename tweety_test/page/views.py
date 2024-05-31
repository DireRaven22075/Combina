from typing import Any
from django.shortcuts import render, redirect
from tweety import Twitter
from .models import Account, Content
from django.contrib import messages
from django.views import View

#auth : author 클래스의 인스턴스.
#user : model 에 저장된 유저 정보.

class author:
    def __init__(self, email="", password=""):
        self.email = email
        self.password = password

    def set(self,email, password):
        self.email = email
        self.password = password
        self.app = Twitter("new_user_session")
        self.app.sign_in(self.email, self.password)
        if Account.objects.filter(email=self.email).exists():
            print("existing_user_session")
            
        else:
            print("new_user_session")
            user = Account.objects.get(
                connect=True,
                name=self.app._username,
                email=self.email, 
                password=self.password,
                platform="twitter")
            user.save()

    def __any__(self):
        return self.app
        
auth = author()




def home(request):
    return render(request, 'template/page/home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        auth.set(email=email, password=password)
        if auth != None:
            messages.success(request, '로그인 성공')
            
            return redirect('/')
        else:
            messages.error(request, '로그인 실패')
    return render(request, 'template/page/login.html')


def search_tweet(request):
    app = auth.__any__()
    if auth is None:
        return redirect('/login')
    if request.method == 'POST':
        
        search = request.POST.get('search')
        search_tweet = app.search(keyword=search, pages=1)[:5]
        tweets = []
        for tweet in search_tweet:
            tweet_detail = app.tweet_detail(tweet['id'])
            if tweet_detail is not None:
                image_list = [] 
                if 'media' in tweet_detail._tweet['legacy']['entities']:
                    for media_item in tweet_detail._tweet['legacy']['entities']['media']:
                        image_list.append(media_item['media_url_https'])
                        
                else:
                    print("no media")
                
                tweets.append({
                    'tweet_name': tweet_detail.author.name,
                    'tweet_username': tweet_detail.author.username,
                    'tweet_text': tweet_detail.text.split('https')[0],
                    'tweet_date': tweet_detail.date,
                    'tweet_media_url': image_list
                })
                print(tweets)
        context = {
            'tweets': tweets
        }
        return render(request, 'template/page/home.html', context)
    return redirect('/')

