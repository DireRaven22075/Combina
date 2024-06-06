from platformEverytime.views import driver_set
from django.shortcuts import render
from page.models import AccountDB, ContentDB, FileDB
from django.contrib.sessions.models import Session



def home(request):
    #로그인 쿠키 없으면 홈 바로 로딩, 있으면 자유게시판 포스트 가져오기
    

    # user = driver_set(request)
    # if user.session_is_exist():
    #     print(f"session in home: {request.session['id'], request.session['password'], request.session['name']}")
    #     list = []
    #     # 현재 오타쿠 게시판 포스트 가져오도록 설정
    #     list = user.image_field(5)
        
    #     for i, post in enumerate(list, start=1):
    #         print(f"post{i} : {post}")
    #         text = post['title']+ "\n" + post['text']
    #         image_url = 0
    #         if post['image'] is not None:
    #             latest = FileDB.objects.latest('uid')
    #             if latest is None:
    #                 image_url = 1
    #             else:
    #                 image_url = latest.uid + 1
                
    #             print(f"url : {image_url}, image : {post['image']}")
    #             file = FileDB.objects.create(
    #                 uid=image_url,
    #                 url=post['image']
    #             )
    #             file.save()
    #         content = ContentDB.objects.create(
    #             platform="everytime",
    #             userID=post['username'],
    #             text=text,
    #             image_url=image_url,
    #             userIcon=None,
    #             vote=post['vote']
    #         )
    #         content.save()
    #     context = {
    #         'post' : list
    #     }

    #     return render(request, 'every/home.html', context)
    
    # else:
    #     print("session not exist")
    return render(request, "every/home.html")

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        user = driver_set(request)
        if user.session_is_exist():
            print(f"session in home: {request.session['id'], request.session['password'], request.session['name']}")
            list = []
            list = user.search_field(search)
            for i, post in enumerate(list, start=1):
                print(f"post{i} : {post}")
                text = post['title']+ "\n" + post['text']
                image_url = 0
                if post['image'] is not None:
                    latest = FileDB.objects.latest('uid')
                    if latest is None:
                        image_url = 1
                    else:
                        image_url = latest.uid + 1
                    
                    print(f"url : {image_url}, image : {post['image']}")
                    file = FileDB.objects.create(
                        uid=image_url,
                        url=post['image']
                    )
                    file.save()
                content = ContentDB.objects.create(
                    platform="everytime",
                    userID=post['username'],
                    text=text,
                    image_url=image_url,
                    userIcon=None,
                    vote=post['vote']
                )
                content.save()
            context = {
                'post' : list
            }

        return render(request, 'every/home.html', context)
    
    else:
        print("There's no input to search")

    return render(request, 'every/home.html')