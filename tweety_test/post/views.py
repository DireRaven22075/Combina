from django.shortcuts import render, redirect  
from tweety import Twitter
from page.models import Account, Content
from page.views import author, auth
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

user_data = []

@login_required
def post(request):
    user = request.user
    if user == None:
        return redirect('../login')
    print(user)
    user_data = [
        user.name,
        user.platform,
    ]
    
    return render(request, 'template/post/post.html')

def create_post(request):
    app = auth.__any__()
    user = Account.objects.get(email = user.email)

    if user == None:
        return redirect('../login')
    if request.method == 'POST':
        post = request.POST.get('post')
        print(post)
        create = app.create_tweet(text=post, file="") #트윗 정보 리턴  
        print(create)
        context = {
            'post' : create,
            'post_text' : create.text
        }
        contents = Content(
            Account = user,
            name = user.name,
            platform = user.platform,
            text = create.text,
            date = create.date,
            icon = create.icon,
            image = create.image,
            tag = create.tag
        )
        contents.save()
        return render(request, 'template/post/post.html', context)
        
        
        
    return redirect('/')