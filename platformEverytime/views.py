from django.shortcuts import render, redirect
from django.http import JsonResponse
from .account import Account
from .content import Content
from .post import Post
from page.models import ContentDB, FileDB, AccountDB
import json
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# 로그인 정보 json으로 받아서 처리
# 에타에서 로그인 토큰 받아오기
# conntect=True javascript 함수 어떻게 할 것인지...
# 현재 로그인 안 한 상태에서 /everytime/가면 json으로 에러 안 뜨ㅢ워짐


# page 값 init , account 확인 및 로그인 상태까지 보내기

MAX_POSTS = 10


class Everytime:
    
    @staticmethod
    def home(request):
        try:
            userAccount = AccountDB.objects.filter(name = request.session['username']).first()
            post_content = ContentDB.objects.filter(platform = "Everytime").order_by('-id')[:MAX_POSTS].values("userID", "text", "image_url", "vote")
            
            for post in post_content:
                
                if post['image_url'] != 0:
                    try:
                        file = FileDB.objects.get(uid = post['image_url'])
                        post['image_url'] = file.url
                    except FileDB.DoesNotExist:
                        post['image_url'] = None

                else:
                    post['image_url'] = None
            return render(request, "every_test/home.html" , {
                'contents': post_content, "username":userAccount.name})
        except Exception as e:
            print(f"error : {e}")
            return render(request, "every_test/home.html")
    
    # 로그인 페이지 렌더링
    @staticmethod
    def login_page(request):
        
        if request.method == 'POST':
            print("get post in login_page")
            page = request.POST.get('page', 'None')  # 기본값 'init'
            print("page : ", page)
            print("page type : ", type(page))

            request.session['page'] = page
            request.session.save()
            print("page saved in session", page)
        
        return render(request, 'every_test/login.html' )
    
    @staticmethod
    def check_login_status(request):
        initial_username = request.session.get('username')
        
        if  initial_username is not None:
            return True
        else:
            return False
    
    @csrf_exempt
    def redirect_page(request):
        if request.method == 'POST':
             
            page = request.session.get('page', 'None')
            connection = Everytime.check_login_status(request)
          
            print("page", page)
            
            if page == 'init':
                url = 'http://127.0.0.1:8000' 
            else:
                url = 'http://127.0.0.1:8000/account'

            response_data = {
                'redirect_url': url,
                'connection': connection
                }
            print(response_data)

            # connect = True 바꾸기
            try:
                userAccount = AccountDB.objects.filter(name = request.session['username']).first()
                if userAccount:
                    AccountDB.objects.filter(name = request.session['username']).update(connected=True)
                    print("connected")
                    return JsonResponse(response_data)  
                else:
                    return JsonResponse({"error":'User not matching'}, status=400)
            except KeyError:
                print("no username in session")
                return JsonResponse(response_data)

        return JsonResponse({'error': 'Invalid request'}, status=400)



    #로그인 처리, 세션 저장과 동시에 컨텐츠 크롤링
    @staticmethod
    async def ev_login(request):
        if request.method == "POST":
          
            id = request.POST.get("id")
            password = request.POST.get("password")
            print(f"id : {id}, password : {password}")
            if not id or not password:
                print("no id or password in sentence")
                return JsonResponse("아이디 또는 비밀번호를 입력하세요.", status=400)
            
            try:
                #세션 저장 
                session_saved = await sync_to_async(Everytime.save_session)(request, id, password)
                if not session_saved:
                    print("session save error")
                    return JsonResponse({"error":"session save error"},status=400)
                user = await sync_to_async(Content)(request)
                print("user : ", user)
                success = await sync_to_async(user.free_field)()
                print("success : ", success)
                if success:
                    return JsonResponse({"connection":"login success"})
                else:
                    print("crawling error")
                    return JsonResponse({"error":"crawling error"},status=200)
                
            except KeyError:
                print("no id or password in KeyError")
                return JsonResponse({"error":"ID or PASSWORD are incorrect"},status=200) # 아이디 혹은 비밀번호 없음

        return JsonResponse({"error":"no post provided"},status=400)    
    
    
    
    # 최신 컨텐츠 가져오기
    @staticmethod
    async def ev_free_field(request):
        if request.method == "POST":
                user = await sync_to_async(Content)(request)
                crawling = await sync_to_async(user.free_field)()
                if crawling:
                    return JsonResponse({"success":"crawling success in free_field"})
                else:
                    return JsonResponse({"error":"crawling error in free_field"},status=400)

        return JsonResponse({"error":"no post provided"})
    
    
    # 게시글 작성 (현재 업로드만 막아둠)
    @staticmethod
    async def ev_post(request):
        if request.method == "POST":
            try:
               
                data = request.POST
                title = request.POST.get('title')
                text = request.POST.get('text')
                image_list = request.FILES.getlist('file')
                
               
                valid = text is not None and title is not None
                if valid:
                    user = await sync_to_async(Post)(request)
                    posting = await sync_to_async(user.post)(title,text, image_list)
                    if posting:
                        return JsonResponse({"success": posting})
                    
                    else:
                        return JsonResponse({"error":"posting error"},status=400)
                        
                else:
                    return JsonResponse({"error":"No text provided"}, status=400)  
            except json.JSONDecodeError:
                return JsonResponse({"error":"Invalid Json data"},status=400)  
        return JsonResponse({"error":"No post in ev_post"},status=400)
    
    # 세션 삭제 및 connect = FAlse
    @staticmethod
    def logout(request):
        try:
            # 처음에 세션 값이 있는지 검사
            initial_ev_id = request.session.get('ev_id')
            initial_ev_password = request.session.get('ev_password')
            initial_username = request.session.get('username')
            AccountDB.objects.filter(name = initial_username).update(connected=False)
            if initial_ev_id is None or initial_ev_password is None or initial_username is None:
                missing_keys = []
                if initial_ev_id is None:
                    missing_keys.append('ev_id')
                if initial_ev_password is None:
                    missing_keys.append('ev_password')
                if initial_username is None:
                    missing_keys.append('username')
                error_message = f"Missing session keys initially: {', '.join(missing_keys)}"
                return JsonResponse({"error": error_message}, status=400)
            
            request.session.pop('ev_id', None)
            request.session.pop('ev_password', None)
            request.session.pop('username', None)

            if request.session.get('ev_id') is not None or request.session.get('ev_password') is not None or request.session.get('username') is not None:
                remaining_keys = []
                if request.session.get('ev_id') is not None:
                    remaining_keys.append('ev_id')
                if request.session.get('ev_password') is not None:
                    remaining_keys.append('ev_password')
                if request.session.get('username') is not None:
                    remaining_keys.append('username')
                error_message = f"Failed to remove session keys: {', '.join(remaining_keys)}"
                return JsonResponse({"error": error_message}, status=400)

            return JsonResponse({"success": "logout success"})

        except Exception as e:
            error_message = f"Error during logout: {str(e)}"
            return JsonResponse({"error": error_message}, status=400)
    
    # 세션 저장
    def save_session(request, id, password):
        try:
             
            request.session['ev_id'] = id
            request.session['ev_password'] = password
            request.session.save()
            return request
        except KeyError:
            return None
    
                
    