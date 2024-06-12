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

class Everytime:
    
    @staticmethod
    def home(request):
        try:
            userAccount = AccountDB.objects.filter(name = request.session['username']).first()
            post_content = ContentDB.objects.filter(platform = "Everytime").order_by('-id')[:5].values("userID", "text", "image_url", "vote")
            
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
        #로그인 안 되어 있으면 에러
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
        
            if page == 'init':
                return render(request, 'every_test/login.html', {'page': 'init'})
        
        return render(request, 'every_test/login.html', {'page': 'None'})
    
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
            page = request.POST.get('page')
            connection = Everytime.check_login_status(request)
            print("page", page)
            
            if page == 'init':
                url = reverse('home')  # Replace empty string with the desired URL path
            else:
                url = reverse('login')

            response_data = {
                'redirect_url': url,
                'connection': connection
                }
            print(response_data)

            # connect = True 바꾸기
            userAccount = AccountDB.objects.filter(name = request.session['username']).first()
            if userAccount:
                AccountDB.objects.filter(name = request.session['username']).update(connected=True)
                print("connected")
                return JsonResponse(response_data)
            return JsonResponse({"error":'User not matching'}, status=400)
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
                    return JsonResponse({"success":"login success"},status=200)
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
                    # queryset = await sync_to_async(ContentDB.objects.filter(platform="Everytime").order_by('-id').values)("userID", "text", "image_url", "vote")

                    # # 결과 슬라이드
                    # post_content = list(queryset[:5])

                                    
                    # for post in post_content:
                        
                    #     if post['image_url'] != 0:
                    #         try:
                    #             file = await sync_to_async(FileDB.objects.get)(uid = post['image_url'])
                    #             post['image_url'] = file.url
                    #         except FileDB.DoesNotExist:
                    #             post['image_url'] = None

                    #     else:
                    #         post['image_url'] = None
                    # print("crawling success in free_field")
                
                    # return JsonResponse({"contents":post_content})
                    return JsonResponse({"success":"crawling success in free_field"})
                else:
                    print("crawling error")
                    return JsonResponse({"error":"crawling error in free_field"},status=400)
                
           

        return JsonResponse({"error":"no post provided"})
    
    
    # 게시글 작성 (현재 업로드만 막아둠)
    @staticmethod
    async def ev_post(request):
        if request.method == "POST":
            try:
                json_data = json.loads(request.body)
                title = json_data.get['title']
                text = json_data.get['text']
                image_list = json_data.get['file']
                

                print(f"title : {title}, text : {text}")
                for image in image_list:
                    print(f"image : {image}")

                valid = text is not None and title is not None
                if valid:
                    user = await sync_to_async(Post)(request)
                    posting = await sync_to_async(user.post)(title,text, image_list)
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
                print(error_message)
                return JsonResponse({"error": error_message}, status=400)

            # 세션 값 삭제
            request.session.pop('ev_id', None)
            request.session.pop('ev_password', None)
            request.session.pop('username', None)

            # 삭제 후 세션 값이 남아 있는지 검사
            if request.session.get('ev_id') is not None or request.session.get('ev_password') is not None or request.session.get('username') is not None:
                remaining_keys = []
                if request.session.get('ev_id') is not None:
                    remaining_keys.append('ev_id')
                if request.session.get('ev_password') is not None:
                    remaining_keys.append('ev_password')
                if request.session.get('username') is not None:
                    remaining_keys.append('username')
                error_message = f"Failed to remove session keys: {', '.join(remaining_keys)}"
                print(error_message)
                return JsonResponse({"error": error_message}, status=400)

            # 성공 메시지
            print("logout success")
            return JsonResponse({"success": "logout success"})

        except Exception as e:
            error_message = f"Error during logout: {str(e)}"
            print(error_message)
            return JsonResponse({"error": error_message}, status=400)
    
    def save_session(request, id, password):
        try:
             
            request.session.create()
            request.session['ev_id'] = id
            request.session['ev_password'] = password
            request.session.save()
            print(f"id : {request.session['ev_id']}, password : {request.session['ev_password']}")
            return request
        except KeyError:
            print("no id or password in session")
            return None
    
                
    # 검색어를 통한 컨텐츠 검색 안씀
    @staticmethod
    async def ev_search_field(request):
        if request.method == "POST":
            # json_data = json.loads(request.body)
            # search = json_data.get('search')
            
            search = request.POST.get("search")
            
            print(f"search : {search}")
            if search is None or len(search) < 2:
                print("검색어는 2글자 이상 입력해주세요.")
                return JsonResponse({"error": "Your should input word at least 2 length"},status=400)
            
            driver = await sync_to_async(Account.login)(request)

            if driver:
                crawling = await sync_to_async(Content.search_field)(search, driver)
                if crawling:
                    #post_content = await sync_to_async(ContentDB.objects.filter(platform="everytime").order_by('-id').values)("userID", "text", "image_url", "vote")[:5]
                    queryset = ContentDB.objects.filter(platform="Everytime").order_by('-id').values("userID", "text", "image_url", "vote")[:5]
                    post_content = await sync_to_async(list)(queryset)

                    for post in post_content:
                        
                        if post['image_url'] != 0:
                            try:
                                file = await sync_to_async(FileDB.objects.get)(uid = post['image_url'])
                                post['image_url'] = file.url
                            except FileDB.DoesNotExist:
                                post['image_url'] = None
                        else:
                            post['image_url'] = None
                    print("crawling success in search_field")
                    return JsonResponse({"contents":post_content})
                else:
                    print("crawling error")
                    return JsonResponse({"error":"crawling error in search_field"},status=400)
            else:
                print("login error")
                return JsonResponse({"error": "driver is None in search_field"},status=400)
            
            
        return JsonResponse({"error":"no search word provided"}, status=400)
        