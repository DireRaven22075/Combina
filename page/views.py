from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def Post(request):
    return render(request, 'post.html')

def Find(request):
    return render(request, 'find.html')

def Chat(request):
    return render(request, 'chat.html')

def InChat(request, platform, id):
    contents = {
        'platform': platform,
        'id': id,
    }
    return render(request, 'inChat.html', contents)

def Menu(request):
    return render(request, 'menu.html')
