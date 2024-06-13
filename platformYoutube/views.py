import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from page.models import AccountDB
from google_auth_oauthlib.flow import InstalledAppFlow
from platformYoutube.auth import get_authenticated_service, login, logout  # Corrected import
from .view_recommended import view_recommended
from .view_profile import view_profile
from .search_videos import search_videos

class YouTubeView:
    REDIRECT_URI = 'http://localhost:8000/youtube/callback/'

    def Connect(request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
            redirect_uri=YouTubeView.REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        request.session['state'] = state
        return redirect(authorization_url)

    def ConnectCallback(request):
        state = request.session['state']
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl'],
            state=state,
            redirect_uri=YouTubeView.REDIRECT_URI
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials

        headers = {'Authorization': f'Bearer {credentials.token}', 'Accept': 'application/json'}
        response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
        if response.status_code != 200:
            return JsonResponse({"status": "error", "message": "Failed to get user info"}, status=400)

        user_data = response.json()
        username = user_data['name']
        icon_img = user_data['picture']

        user = AccountDB.objects.filter(platform="YouTube").first()
        if not user:
            user = AccountDB(platform="YouTube")
        user.name = username
        user.token = credentials.token
        user.connected = True
        user.icon = icon_img
        user.tag = username
        user.save()

        return render(request, 'youtube/close_window.html')

    def Disconnect(request):
        user = AccountDB.objects.filter(platform="YouTube").first()
        if user:
            user.name = None
            user.token = None
            user.connected = False
            user.icon = None
            user.tag = None
            user.save()
        return redirect(request.META.get('HTTP_REFERER', '/home'))

    def GetContent(request):
        user = AccountDB.objects.filter(platform="YouTube").first()
        if not user or not user.token:
            return JsonResponse({"status": "error", "message": "Not connected to YouTube"}, status=400)

        headers = {'Authorization': f'Bearer {user.token}', 'Accept': 'application/json'}

        content_type = request.GET.get('type')
        limit = int(request.GET.get('limit', 5))

        if content_type == 'recommended':
            content = view_recommended(limit)
        elif content_type == 'search':
            query = request.GET.get('query')
            content = search_videos(query)
        else:
            return JsonResponse({"status": "error", "message": "Invalid content type"}, status=400)

        return JsonResponse(content, safe=False)
