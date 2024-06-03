from django.shortcuts import render, redirect  
from tweety import Twitter
from page.models import Account, Content
from page.views import author, auth
from .models import Post
from django.contrib.auth.decorators import login_required
# from .forms import TweetForm

# Create your views here.

user_data = []

@login_required
def post(request):

    user = request.user
    print(user)
    if user == None:
        return redirect('../login')
    print(user)
    # user_data = [
    #     user.name,
    #     user.platform,
    # ]
    
    return render(request, 'template/post/post.html')

def create_post(request):
    app = auth.__any__()
    user = Account.objects.get(email = 'ricecracke77108')
    if user == None:
        return redirect('../login')

    if user == None:
        return redirect('../login')
    if request.method == 'POST':
        post = request.POST.get('post')
        image = request.FILES.get('image')
        
        print(post)
        # Save the image file
        #image_path = ""
        print(image)
        create = app.create_tweet(text=post, files=[f"{image}"]) #트윗 정보 리턴  
        print(create)
        context = {
            'post' : create,
            'post_text' : create.text,
            'post_image' : create.image,
        }
        # contents = Content(
        #     Account = user,
        #     name = user.name,
        #     platform = user.platform,
        #     text = create.text,
        #     date = create.date,
        #     icon = create.icon,
        #     image = create.image,
        #     tag = create.tag
        # )
        # contents.save()
        return render(request, 'template/post/post.html', context)
    return redirect('/')