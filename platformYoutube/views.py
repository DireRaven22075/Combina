import os
import pickle
import logging
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from .auth import get_authenticated_service
from .view_profile import view_profile
# from .view_recommended import view_recommended  # Disable this import for now
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
        """ Disconnects the YouTube account and removes tokens """
        user = AccountDB.objects.filter(platform="Youtube").first()
        if user:
            user.name = None
            user.token = None
            user.connected = False
            user.icon = None
            user.tag = None
            user.save()
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')
        return redirect('/home')

    @staticmethod
    def ClearContent(request):
        """ Clears all YouTube related content from ContentDB and FileDB """
        ContentDB.objects.filter(platform="Youtube").delete()
        FileDB.objects.filter(uid__in=ContentDB.objects.filter(platform="Youtube").values_list('id', flat=True)).delete()
        return JsonResponse({'status': 'success'}, safe=False)

    @staticmethod
    def GetContent(request):
        """ Placeholder for GetContent method """
        return JsonResponse({'status': 'success'}, safe=False)
