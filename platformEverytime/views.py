from django.shortcuts import render, redirect
from django.http import HttpResponse
from .account import Account
from .content import Content
from .post import Post
from page.models import ContentDB, FileDB
import json


class Everytime:

    @staticmethod
    def home(request):
        return render(request, "every/home.html")
    
    @staticmethod
    def ev_login(request):
        if request.method == "POST":
            id = request.POST.get("id")
            password = request.POST.get("password")
            try:
                #세션 저장 비동기화
                Everytime.save_session(request, id, password)
                
                # 로그인처리 비동기화
                driver = Account.login(request)
                print(f"session in user name: {request.session['username']}")
                if driver is not None:
                    print("Account success")
                    Content.free_field(request,driver)
                    
                    driver.quit()
                    return redirect('/')
                else:
                    print("login error, try again")
            except KeyError:
                print("no id or password")
                return HttpResponse(status=200) # 아이디 혹은 비밀번호 없음
            
        return render(request, "every/login.html")
    
    @staticmethod
    def ev_logout(request):
        request.session.flush()
        return render(request, "every/login.html")
    
    @staticmethod
    def ev_free_field(request):
        #driver = Account(request.session['id'], request.session['password']).__any__()
        #driver = Account.login(request)
        #Content.free_field(request, driver)
        post_content = ContentDB.objects.filter(platform = "everytime").order_by('-id')[:5]
        upload = []

        for post in post_content:
            image_url = 0
            if post.image_url != 0:
                try:
                    file = FileDB.objects.get(uid = post.image_url)
                    image_url = file.url
                except FileDB.DoesNotExist:
                    print("file is not exist")
                    image_url = 0
            upload.append({
                'text':post.text,
                'user' : post.userID,
                'vote' : post.vote,
                'image' : image_url
            })
        return render(request, "every/home.html" , {'upload':upload})
    
    @staticmethod
    def ev_search_field(request):
        if request.method == "POST":
            search = request.POST.get('search')
            driver = Account.login(request)
            Content.search_field(request, search=search, driver=driver)
            
            post_content = ContentDB.objects.filter(platform = "everytime").order_by('-id')[:5]
            upload = []
            for post in post_content:
                image_url = 0
                if post.image_url != 0:
                    try:
                        file = FileDB.objects.get(uid = post.image_url)
                        image_url = file.url
                    except FileDB.DoesNotExist:
                        print("file is not exist")
                        image_url = 0
                upload.append({
                    'text':post.text,
                    'user' : post.userID,
                    'vote' : post.vote,
                    'image' : image_url
                })
        return render(request, "every/home.html")
    
    @staticmethod
    def ev_post(request):
        if request.method == "POST":
            try:
               
                text = request.POST.get('text')
                images = request.FILES.getlist('image')

                print(f"text : {text}, images : {images}")
                if text is not None:
                    driver = Account.login(request)
                    Post.post(request, text, images, driver)
                    return render(request, "every/home.html")
                
                else:
                    print("No text provided")
                    return HttpResponse(status=400)  # Bad Request: 요청이 부적절한 경우
            except json.JSONDecodeError:
                print("Invalid JSON data")
                return HttpResponse(status=400)  # Bad Request: 요청이 부적절한 경우
        return render(request, "every/post.html")
    
    
    @staticmethod
    def save_session(request, id, password):
        try:
            request.session.create()
            request.session['id'] = id
            request.session['password'] = password
            request.session.save()
            print(f"id : {request.session['id']}, password : {request.session['password']}")
            return request
        except KeyError:
            print("no id or password")
            return None
       
        