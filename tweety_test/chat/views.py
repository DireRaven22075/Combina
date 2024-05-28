from django.shortcuts import render, redirect
from tweety import Twitter

# Create your views here.
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
path = os.path.abspath(os.path.join(current_directory, '../password.txt'))
f = open(path)
email = f.readline()
password = f.readline()
print(email, password)
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
        return render(request, 'template/chat/chat.html', context)
    return redirect('/')
