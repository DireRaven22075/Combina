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
from .view_recommended import view_recommended
from .search_videos import search_videos
from page.models import AccountDB
from page.views import parameters

# Allow insecure transport for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class YouTubeView:
    REDIRECT_URI = 'http://localhost:8000/Youtube/callback/'
    SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
    CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client_secret.json')

    def Connect(request):
        flow = Flow.from_client_secrets_file(
            YouTubeView.CLIENT_SECRETS_FILE, scopes=YouTubeView.SCOPES)
        flow.redirect_uri = YouTubeView.REDIRECT_URI
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        request.session['state'] = state
        request.session.save()
        logger.debug(f"Connect: Saved state {state} in session")
        return redirect(authorization_url)

    def ConnectCallback(request):
        stored_state = request.session.get('state')
        state = request.GET.get('state')

        logger.debug(f"ConnectCallback: Retrieved state {stored_state} from session")
        logger.debug(f"ConnectCallback: State from request {state}")

        if state != stored_state:
            logger.error(f"State mismatch: expected {stored_state}, got {state}")
            return JsonResponse({"status": "error", "message": "State parameter mismatch"}, status=400)
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
        user.tag = user_info['title']
        user.save()
        return render(request, 'page/welcome2.html', parameters())

    def Disconnect(request):
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

    def GetContent(request):
        user = AccountDB.objects.filter(platform="Youtube").first()
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
