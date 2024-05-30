from django.shortcuts import render, redirect  
from tweety import Twitter
from page.models import Account, Content
from django.views import View
from page.views import author
from page.views import user
# Create your views here.



def post(request):
    return render(request, 'template/post/post.html')

def create_post(request):
    app = user.__any__()
    if user == None:
        return redirect('../login')
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