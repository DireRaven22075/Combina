from django.shortcuts import render, redirect
from django.http import JsonResponse
from .account import Account
from .content import Content
from page.models import ContentDB, FileDB, AccountDB
from .webdriver_manager import WebDriverManager
import json
from asgiref.sync import sync_to_async
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from selenium.common.exceptions import WebDriverException, TimeoutException


# page 값 init , account 확인 및 로그인 상태까지 보내기
# driver가 없을 때 로그인화면으로 이동

MAX_POSTS = 10
LOGIN_STATUS = True

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
            return render(request, "every_test/home.html")
    
    # 로그인 페이지 렌더링
    @staticmethod
    def login_page(request):
        
        if request.method == 'POST':
            page = request.POST.get('page', 'None')  # 기본값 'init'

            request.session['page'] = page
            request.session.save()
        
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
          
            
            if page == 'init':
                url = 'http://127.0.0.1:8000' 
            else:
                url = 'http://127.0.0.1:8000/accounts'

            response_data = {
                'redirect_url': url,
                'connection': connection
                }

            # connect = True 바꾸기
            try:
                userAccount = AccountDB.objects.filter(name = request.session['username']).first()
                if userAccount:
                    AccountDB.objects.filter(name = request.session['username']).update(connected=True)
                    return JsonResponse(response_data)  
                else:
                    return JsonResponse({"error":'User not matching'}, status=400)
            except KeyError:
                return JsonResponse(response_data)

        return JsonResponse({'error': 'Invalid request'}, status=400)



    #로그인 처리, 세션 저장과 동시에 컨텐츠 크롤링
    @staticmethod
    async def ev_login(request):
        if request.method == "POST":  
            try:
                try:
                    driver = Everytime.driver_manager.get_driver()
                    
                    

                except WebDriverException:
                    Everytime.driver_manager.stop_driver()
                    driver = Everytime.driver_manager.get_driver()
                    return JsonResponse({"error":"driver is not stable, try again"},status=400)  
                except:
                    Everytime.driver_manager.stop_driver()
                    driver = Everytime.driver_manager.get_driver()
                    return JsonResponse({"error":"driver is not stable, try again"},status=400)

                user = await sync_to_async(Account)(request, driver)

                if not user:
                    return JsonResponse({"error":"Account error"},status=200)
                
                Everytime.driver_manager.switch_to_headless()
                return redirect('/start')
            except KeyError:
                return JsonResponse({"error":"ID or PASSWORD are incorrect"},status=200) # 아이디 혹은 비밀번호 없음

        return JsonResponse({"error":"no post provided"},status=400)    
    
    
    
    
    # 최신 컨텐츠 가져오기 왜 세부 컨텐츠를 못 불러오는가?
    # 크롬 드라이버 강제 종료시 왜 driver가 남는가
    @staticmethod
    async def ev_free_field(request):
        if request.method == "POST":
            if Everytime.driver_manager.is_stable():    
                driver = Everytime.driver_manager.get_driver()
                if driver is None: 
                    return redirect(reverse('login'))
                
                
                crawling = await sync_to_async(Content)(driver)
                if crawling:
                    return JsonResponse({"success":"crawling success in free_field"})
                else:
                    return JsonResponse({"error":"crawling error in free_field"},status=400)
            else:
                return redirect(reverse('login'))
        return JsonResponse({"error":"no post provided"})
    
    
  
    @staticmethod
    def logout(request):
        try:
            if Everytime.driver_manager.is_stable():
                Everytime.driver_manager.stop_driver()
           
                
            
            # 처음에 세션 값이 있는지 검사
            if request.session.get('username') is not None:
                initial_username = request.session.get('username')
                account = AccountDB.objects.filter(name = initial_username).first()
                if account:
                    account.name = ''
                    account.connected = False
                    account.token = ''
                    account.tag = ''
                    account.save()
                   
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
            
            return redirect('http://127.0.0.1:8000/accounts')


        except Exception as e:
            error_message = f"Error during logout: {str(e)}"
            return JsonResponse({"error": error_message}, status=400)
    

    
                
    