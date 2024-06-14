from django.shortcuts import render, redirect
from django.http import JsonResponse
from .account import Account
from .content import Content, temp
from .post import Post
from page.models import ContentDB, FileDB, AccountDB
from .webdriver_manager import WebDriverManager
import json
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# 로그인 정보 json으로 받아서 처리
# 에타에서 로그인 토큰 받아오기
# conntect=True javascript 함수 어떻게 할 것인지...
# 현재 로그인 안 한 상태에서 /everytime/가면 json으로 에러 안 뜨ㅢ워짐


# page 값 init , account 확인 및 로그인 상태까지 보내기
# driver가 없을 때 로그인화면?

MAX_POSTS = 10


class Everytime:
    driver_manager = WebDriverManager.get_instance()
    
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
            try:
                driver = Everytime.driver_manager.get_driver()
                
                user = await sync_to_async(Account)(request, driver)
                print("user : ", user)
                if not user:
                    print("Account error")
                    return JsonResponse({"error":"Account error"},status=200)
                
                crawling = await sync_to_async(Content)(driver)
                print("success : ", crawling)
                if crawling:
                    return JsonResponse({"connection":"crawling success"})
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
            if Everytime.driver_manager.is_stable():    
                driver = Everytime.driver_manager.get_driver()
                if driver is None: # 수정 필요
                    print("driver is None")
                    return redirect(reverse('login'))
                
                
                crawling = await sync_to_async(temp)(driver)
                if crawling:
                    return JsonResponse({"success":"crawling success in free_field"})
                else:
                    return JsonResponse({"error":"crawling error in free_field"},status=400)
            else:
                print("driver is not stable")
                return redirect(reverse('login'))
        return JsonResponse({"error":"no post provided"})
    
    
    # # 게시글 작성 (현재 업로드만 막아둠)
    # @staticmethod
    # async def ev_post(request):
    #     if request.method == "POST":
    #         if Everytime.driver_manager.is_stable(): 
    #             driver = Everytime.driver_manager.get_driver()   
    #             try:
                    
                    
    #                 title = request.POST.get('title')
    #                 text = request.POST.get('text')
    #                 image_list = request.FILES.getlist('file')
    #                 print("title : ", title, text, image_list)
                
    #                 valid = text is not None and title is not None
    #                 print("text valid : ", valid)
    #                 if valid:
    #                     posting = await sync_to_async(Post)(driver, title, text, image_list)
    #                     if posting:
    #                         print("posting : ", posting)
    #                         return JsonResponse({"success": posting})
                        
    #                     else:
    #                         print("posting error")
    #                         return JsonResponse({"error":"posting error"},status=400)
                            
    #                 else:
    #                     return JsonResponse({"error":"No text provided"}, status=400)  
    #             except json.JSONDecodeError:
    #                 return JsonResponse({"error":"Invalid Json data"},status=400)
    #         else:
    #             print("driver is not stable")
    #             return redirect(reverse('login'))
    #     return JsonResponse({"error":"No post in ev_post"},status=400)
    
  
    @staticmethod
    def logout(request):
        try:
            if Everytime.driver_manager.is_stable():
                Everytime.driver_manager.stop_driver()
            
            # 처음에 세션 값이 있는지 검사
            if request.session.get('username') is not None:
                initial_username = request.session.get('username')
                AccountDB.objects.filter(name = initial_username).update(connected=False)
                if initial_username is None:
                    missing_keys = []
                    if initial_username is None:
                        missing_keys.append('username')
                    error_message = f"Missing session keys initially: {', '.join(missing_keys)}"
                    return JsonResponse({"error": error_message}, status=400)
                
                request.session.pop('username', None)

                if request.session.get('username') is not None:
                    remaining_keys = []
                    remaining_keys.append('username')
                    error_message = f"Failed to remove session keys: {', '.join(remaining_keys)}"
                    return JsonResponse({"error": error_message}, status=400)
            
            referer = request.META.get('HTTP_REFERER')
            print("referer : ", referer)
            return redirect(request.META.get('HTTP_REFERER', '/home'))


        except Exception as e:
            error_message = f"Error during logout: {str(e)}"
            return JsonResponse({"error": error_message}, status=400)
    
    # 세션 저장 수정 필요
    # def save_session(request, id, password):
    #     try:
             
    #         request.session['ev_id'] = id
    #         request.session['ev_password'] = password
    #         request.session.save()
    #         return request
    #     except KeyError:
    #         return None
    
                
    