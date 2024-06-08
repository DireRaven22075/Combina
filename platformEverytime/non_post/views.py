from django.shortcuts import render, redirect
from page.models import AccountDB, ContentDB, FileDB
from platformEverytime.views import driver_set


# 새글 작성 //*[@id="writeArticleButton"]

def post(request):
    if request.method == "POST":
        print("post start", request.POST)
        user = driver_set(request)
        if user.session_is_exist():
            print(f"session in post: {request.session['id'], request.session['password'], request.session['name']}")
            text = request.POST.get("text")
            image = request.POST.get("image")
            image_url = 0
            print(f"text : {text}, image : {image}")
            if text is None:
                return render(request, "every/post.html")
            
            text_length = "\n" in text
            print(f"text_length : {text_length}")

            if text_length is True:
                if image is None:
                    image_url = 0
                else:
                    latest = FileDB.objects.latest('uid')
                    if latest is None:
                        image_url = 1
                    else:
                        image_url = 1 + latest.uid
                    print(f"text : {text}, image : {image}")
                    file = FileDB.objects.create(
                        uid=image_url,
                        url=image
                    )
                    file.save()

                content = ContentDB.objects.create(
                    platform="everytime",
                    userID=request.session['name'],
                    text=text,
                    image_url=image_url,
                    userIcon=None,
                    vote=0
                )
                content.save()
                post = user.post(text, image)
                context = {
                    'post' : post
                }
                return render(request, "every/post.html", context)
            
            
    return render(request, "every/post.html")