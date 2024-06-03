from django.shortcuts import render, redirect  
from tweety import Twitter
from page.models import Account
from page.views import author, auth
from .models import Post
from .forms import TweetForm
from django.conf import settings

#from django.contrib.auth.decorators import login_required #관리자 상태로 로그인 유지
# from .forms import TweetForm

# Create your views here.

user_data = []


def post(request):

    user = request.user
    print(user)
    if user == None:
        return redirect('../login')
    print(user)
    
    return render(request, 'template/post/post.html')

# 경로 찾아서 저장
import os
def handle_uploaded_file(f, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path
    
def create_post(request):
    app = auth.__any__()
    print(f"auth : {auth.__any__()}\nemail: {auth.email}") 
    user = Account.objects.get(email=auth.email)

    if user and app is None:
        return redirect('../login')
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            post = form.save(commit=False)
            images = []
            file_path = ""
            for i in range(1, 2):
                print("iamge save  ----")
                image = request.FILES.get(f'image')
                if image:
                    print("file path -----")
                    filename = f'image{i}_{image.name}'
                    file_path = handle_uploaded_file(image, filename)
                    print(f"file path in image save : {file_path}")
                    images.append(file_path)
            post.images = images
            post.save()
            #트윗 보내기
            print(f"post path : {file_path} ,{type(file_path)}\n\n")
            print(f"post image : {type(post.image)}\n\n")
            print(f"file path in create tweet: {file_path}\n\n")
            #image_path = os.join(settings.BASE_DIR, f"{post.image}")
            context = app.create_tweet(
                text = post.text,
                files = [f"{file_path}"]
            )
            

        return render(request, 'template/post/post.html')
    else:
        print("fail get POST")
        form = TweetForm()

    return redirect('/')