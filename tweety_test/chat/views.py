from django.shortcuts import render, redirect
from tweety import Twitter
# Create your views here.

email = 'ricecracke77108'
password = 'hayeon1806x'
app = Twitter("session")
app.sign_in(email, password)



def chat(request):
    return render(request, 'template/chat/chat.html')

def chat_log(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        message = request.POST.get('message')
        print(username, message)
        chat = app.send_message(username, message)
        context = {
            'chat': chat,
            'username' : username,
            'message' : message
        }
        print(context)
        return render(request, 'template/chat/chat.html', context)
    return redirect('/')
