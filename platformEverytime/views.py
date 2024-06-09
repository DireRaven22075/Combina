from django.shortcuts import render, redirect
from django.http import JsonResponse
from .account import Account
from .content import Content
from .post import Post
from page.models import ContentDB, FileDB, AccountDB
import json



class Everytime:

    @staticmethod
    def home(request):
        userAccount = AccountDB.objects.filter(name = request.session['username']).first()
        post_content = ContentDB.objects.filter(platform = "everytime").order_by('-id')[:5].values("userID", "text", "image_url", "vote")
        
        for post in post_content:
            
            if post['image_url'] != 0:
                try:
                    file = FileDB.objects.get(uid = post['image_url'])
                    post['image_url'] = file.url
                except FileDB.DoesNotExist:
                    post['image_url'] = None

            else:
                post['image_url'] = None
            # upload.append({
            #     'text':post.text,
            #     'user' : post.userID,
            #     'vote' : post.vote,
            #     'image' : image_url
            # })
            # print("current upload : ",upload)
        return render(request, "every_test/home.html" , {
            'contents': post_content, "username":userAccount.name})
    
    #로그인 처리, 세션 저장과 동시에 컨텐츠 크롤링
    @staticmethod
    def ev_login(request):
        if request.method == "POST":
            id = request.POST.get("id")
            password = request.POST.get("password")
            if not id or not password:
                print("no id or password")
                return JsonResponse("아이디 또는 비밀번호를 입력하세요.", status=400)
            
            try:
                #세션 저장 
                Everytime.save_session(request, id, password)
                
                driver = Account.login(request)
                if driver:
                    print("Account success")
                    crawling =Content.free_field(driver)
                    if crawling:
                        return redirect('/every/')
                    else:
                        print("crawling error")
                        return JsonResponse({"error":"crawling error"},status=200)
                else:
                    print("login error, try again")
                    return JsonResponse({"error":"driver is None"},status=200)
            except KeyError:
                print("no id or password")
                return JsonResponse({"error":"ID or PASSWORD are incorrect"},status=200) # 아이디 혹은 비밀번호 없음
            
        return render(request, "every_test/login.html")
    
    
    # 최신 컨텐츠 가져오기
    @staticmethod
    def ev_free_field(request):
        if request.method == "POST":
            
            # 최신 컨텐츠 새로고침시
            driver = Account.login(request)
            if driver:

                crawling = Content.free_field(driver)
                if crawling:
                    print("crawling success in free_field")
                    return JsonResponse({"contents":True})
                else:
                    print("crawling error")
                    return JsonResponse({"error":"crawling error in free_field"},status=400)
                
            else:
                print("login error")
                return JsonResponse({"error": "driver is None in ev_free_field function"}, status=400)

        return JsonResponse({"error":"no post provided"})
    
    # 검색어를 통한 컨텐츠 검색
    @staticmethod
    def ev_search_field(request):
        if request.method == "POST":
            search = request.POST.get('search')
            print(f"search : {search}")
            if search is None or len(search) < 2:
                print("검색어는 2글자 이상 입력해주세요.")
                return JsonResponse({"error": "Your should input word at least 2 length"},status=400)
            
            driver = Account.login(request)

            if driver:
                crawling = Content.search_field(search, driver)
                if crawling:
                    return JsonResponse({"success":True})
                else:
                    print("crawling error")
                    return JsonResponse({"error":"crawling error in search_field"},status=400)
            else:
                print("login error")
                return JsonResponse({"error": "driver is None in search_field"},status=400)
            
            
        return JsonResponse({"error":"no search word provided"}, status=400)
    
    # 게시글 작성 (현재 업로드만 막아둠)
    @staticmethod
    def ev_post(request):
        if request.method == "POST":
            try:
               
                text = request.POST.get('text')
                images = request.FILES.getlist('image')

                print(f"text : {text}, images : {images}")
                valid = '\n' in text
                if valid:
                    driver = Account.login(request)
                    if driver is None:
                        print("login error")
                        return JsonResponse({"error":"driver is None in post"},status=400)
                    
                    posting = Post.post(text, images, driver)
                    if posting:
                        print("posting success")
                        return JsonResponse({"success": posting})
                    
                    else:
                        return JsonResponse({"error":"posting error"},status=400)
                        
                else:
                    print("No text provided")
                    return JsonResponse({"error":"No text provided"}, status=400)  # Bad Request: 요청이 부적절한 경우
            except json.JSONDecodeError:
                print("Invalid JSON data")
                return JsonResponse({"error":"Invalid Json data"},status=400)  # Bad Request: 요청이 부적절한 경우
        return JsonResponse({"error":"No post in ev_post"},status=400)
    
    
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
       
    
        