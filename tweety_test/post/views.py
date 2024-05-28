from django.shortcuts import render, redirect  
from tweety import Twitter
from page.models import Account, Content
# Create your views here.

email = 'ricecracke77108'
password = 'hayeon1806x'
app = Twitter("session")
app.sign_in(email, password)


def post(request):
    return render(request, 'template/post/post.html')

def create_post(request):
    if request.method == 'POST':
        post = request.POST.get('post')
        print(post)
        create = app.create_tweet(text=post) #트윗 정보 리턴  
        print(create)
        context = {
            'post' : create,
            'post_text' : create.text
        }
        return render(request, 'template/post/post.html', context)
        
        
        
    return redirect('/')