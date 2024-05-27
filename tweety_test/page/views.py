from django.shortcuts import render, redirect
from tweety import Twitter
from .models import Account, Content
from django.contrib import messages

email = 'ricecracke77108'
password = 'hayeon1806x'
app = Twitter("session")
user = app.sign_in(email, password)



def home(request):
    # search_tweet = app.search(keyword='안모리', pages=1)[:5]
    # tweets = []
    # for tweet in search_tweet:
    #     tweet_detail = app.tweet_detail(tweet['id'])
    #     if tweet_detail is not None:
    #         tweets.append({
    #             'tweet_name': tweet_detail.author.name,
    #             'tweet_username': tweet_detail.author.username,
    #             'tweet_text': tweet_detail.text,
    #             'tweet_date': tweet_detail.date
    #         })
    # context = {
    #     'tweets': tweets
    # }
    
    # print(context)
    return render(request, 'template/page/home.html')

def login(request):
    return render(request, 'template/page/login.html')

def search_tweet(request):
    if request.method == 'POST':
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
        context = {
            'tweets': tweets
        }
        return render(request, 'template/page/home.html', context)
    return redirect('/')


# def home(request):
#     if Account.connect == 0:
#         return redirect('/login')
#     else:
#         tweet()
    
#     return render(request, 'template/page/home.html')

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
        
#         user = app.sign_in(f'{email}',f'{password}')
#         if user != None:
#             messages.success(request, '로그인 성공')
#             Account.objects.create(email=email, password=password, connect =1)
#             Account.save()
#             return redirect('')
#         else:
#             messages.error(request, '로그인 실패')
        
#     return render(request, 'template/page/login.html')

# def tweet(request):
#     if request.method == 'POST':
#         text = request.POST.get('text')
#         Twitter.tweet(text)
#         return redirect('/home')
#     return render(request, 'template/page/tweet.html')