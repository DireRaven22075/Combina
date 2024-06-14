import os
import pickle
import logging
import requests
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from .auth import get_authenticated_service
from .view_profile import view_profile
from .search_videos import search_recommended_videos
from page.models import AccountDB, ContentDB, FileDB
from page.views import parameters

# Allow insecure transport for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class YouTubeView:
    REDIRECT_URI = 'http://localhost:8000/Youtube/callback/'
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
    CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')

    @staticmethod
    def Connect(request):
        """ Initiates the OAuth flow for YouTube """
        flow = Flow.from_client_secrets_file(
            YouTubeView.CLIENT_SECRETS_FILE, scopes=YouTubeView.SCOPES)
        flow.redirect_uri = YouTubeView.REDIRECT_URI
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        request.session['state'] = state
        request.session.save()
        logger.debug(f"Connect: Saved state {state} in session")
        return redirect(authorization_url)

    @staticmethod
    def ConnectCallback(request):
        """ Handles the OAuth callback from YouTube """
        state = request.GET.get('state')

        try:
            flow = Flow.from_client_secrets_file(
                YouTubeView.CLIENT_SECRETS_FILE, scopes=YouTubeView.SCOPES, state=state)
            flow.redirect_uri = YouTubeView.REDIRECT_URI
            flow.fetch_token(authorization_response=request.build_absolute_uri())
            credentials = flow.credentials

            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

            youtube_service = build('youtube', 'v3', credentials=credentials)
            response = youtube_service.channels().list(
                mine=True, part='snippet').execute()
            user_info = response['items'][0]['snippet']
            user = AccountDB.objects.filter(platform="Youtube").first()
            if not user:
                user = AccountDB(platform="Youtube")
            user.name = user_info['title']
            user.token = credentials.token
            user.connected = True
            user.icon = user_info['thumbnails']['default']['url']
            user.tag = user_info.get('customUrl', '')  # Update this if needed
            user.save()

            return render(request, 'page/00_welcome2.html', parameters())
        except Exception as e:
            logger.error(f"Exception during OAuth callback: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    @staticmethod
    def Disconnect(request):
        user = AccountDB.objects.filter(platform="Youtube").first()
        user.name = ""
        user.token = ""
        user.connected = False
        user.icon = "http://default.url/icon"
        user.tag = ""
        user.save()
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')
        return redirect('http://127.0.0.1:8000/accounts', cookies={'csrftoken', get_token(request)})

    @staticmethod
    def ClearContent(request):
        """ Clears all YouTube related content from ContentDB and FileDB """
        FileDB.objects.filter(uid__in=ContentDB.objects.filter(platform="Youtube").values_list('id', flat=True)).delete()
        ContentDB.objects.filter(platform="Youtube").delete()
        return JsonResponse({'status': 'success'}, safe=False)

    @staticmethod
    def GetContent(request):
        """ Fetches new content after clearing existing content """
        YouTubeView.ClearContent(request)
        
        # Fetch new content
        videos = search_recommended_videos()
        
        return JsonResponse(videos, safe=False)
