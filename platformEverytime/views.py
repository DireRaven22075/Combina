from django.shortcuts import render, redirect
from django.http import JsonResponse
from .account import Account
from .content import Content
from .post import Post
from page.models import ContentDB, FileDB, AccountDB
import json
from asgiref.sync import sync_to_async


# 로그인 정보 json으로 받아서 처리
# 에타에서 로그인 토큰 받아오기
# 에타 쿠키 완전 삭제
# 로그아웃 추가
#

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
        return render(request, "every_test/home.html" , {
            'contents': post_content, "username":userAccount.name})
    
    #로그인 처리, 세션 저장과 동시에 컨텐츠 크롤링
    @staticmethod
    def ev_login(request):
        if request.method == "POST":
            # try:
            # # 요청의 본문을 변수에 저장
            #     request_body = request.body
                
            #     json_data = json.loads(request_body)
            #     # Check if the JSON data is valid
            #     if not isinstance(json_data, dict):
            #         print("Invalid JSON data in instance")
                    
            # except json.JSONDecodeError:
            #     print("Invalid JSON data in error")
            #     return JsonResponse("잘못된 JSON 데이터입니다.", status=400)

            id = request.POST.get("id")
            password = request.POST.get("password")
            print(f"id : {id}, password : {password}")
            if not id or not password:
                print("no id or password in sentence")
                return JsonResponse("아이디 또는 비밀번호를 입력하세요.", status=400)
            
            try:
                #세션 저장 
                session_saved = Everytime.save_session(request, id, password)
                if not session_saved:
                    print("session save error")
                    return JsonResponse({"error":"session save error"},status=400)
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
                print("no id or password in KeyError")
                return JsonResponse({"error":"ID or PASSWORD are incorrect"},status=200) # 아이디 혹은 비밀번호 없음
            
        return render(request, "every_test/login.html")
    
    
    # 최신 컨텐츠 가져오기
    @staticmethod
    async def ev_free_field(request):
        if request.method == "POST":
            
            # 최신 컨텐츠 새로고침시
            driver = await sync_to_async(Account.login)(request)
            if driver:

                crawling = await sync_to_async(Content.free_field)(driver)
                if crawling:
                    #post_content = await sync_to_async(ContentDB.objects.filter(platform="everytime").order_by('-id').values)("userID", "text", "image_url", "vote")[:5]
                    queryset = ContentDB.objects.filter(platform="everytime").order_by('-id').values("userID", "text", "image_url", "vote")[:5]
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
                    print("crawling success in free_field")
                    return JsonResponse({"contents":post_content})
                else:
                    print("crawling error")
                    return JsonResponse({"error":"crawling error in free_field"},status=400)
                
            else:
                print("login error")
                return JsonResponse({"error": "driver is None in ev_free_field function"}, status=400)

        return JsonResponse({"error":"no post provided"})
    
    # 검색어를 통한 컨텐츠 검색
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
                    queryset = ContentDB.objects.filter(platform="everytime").order_by('-id').values("userID", "text", "image_url", "vote")[:5]
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
    
    # 게시글 작성 (현재 업로드만 막아둠)
    @staticmethod
    async def ev_post(request):
        if request.method == "POST":
            try:
                # json_data = json.loads(request.body)
                # text = json_data.get('text')
                # images = json_data.get('image')

                text = request.POST.get("text")
                images = request.FILES.getlist("image")

                print(f"text : {text}, images : {images}")
                valid = '\n' in text
                if valid:
                    driver = await sync_to_async(Account.login)(request)
                    if driver is None:
                        print("login error")
                        return JsonResponse({"error":"driver is None in post"},status=400)
                    
                    posting = await sync_to_async(Post.post)(text, images, driver)
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
    
    
    def save_session(request, id, password):
        try:
            # if request.session['ev_id'] is not None or request.session['ev_password'] is not None:
            #     print("session already exists")
            #     request.session.pop('ev_id', None)  # 'ev_id'가 존재하면 삭제
            #     request.session.pop('ev_password', None)  # 'ev_password'가 존재하면 삭제
            #     request.session.pop('username', None)  # 'username'이 존재하면 삭제
            
            request.session.create()
            request.session['ev_id'] = id
            request.session['ev_password'] = password
            request.session.save()
            print(f"id : {request.session['ev_id']}, password : {request.session['ev_password']}")
            return request
        except KeyError:
            print("no id or password in session")
            return None
    
    @staticmethod
    def logout(request):
        try:
            # 처음에 세션 값이 있는지 검사
            initial_ev_id = request.session.get('ev_id')
            initial_ev_password = request.session.get('ev_password')
            initial_username = request.session.get('username')
            
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
                
        