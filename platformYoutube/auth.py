from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build
from page.models import AccountDB

# Define client details directly
CLIENT_ID = "1093025684898-1kdj5micd00haaeo3g0kr9n9fep49fev.apps.googleusercontent.com"
CLIENT_SECRET = "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"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
REDIRECT_URI = "http://localhost:8000/youtube/callback/"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
TOKEN_PATH = "/absolute/path/to/token.pickle"  # 절대 경로로 설정

# Configuration for OAuth 2.0
client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": AUTH_URI,
        "token_uri": TOKEN_URI,
        "redirect_uris": [REDIRECT_URI]
    }
}

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = Flow.from_client_config(client_config, SCOPES)
            flow.redirect_uri = REDIRECT_URI
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(credentials, token)
    return build('youtube', 'v3', credentials=credentials)

def login():
    try:
        service = get_authenticated_service()
        credentials = service._http.credentials
        user = AccountDB.objects.filter(platform="YouTube").first()
        if user:
            user.token = credentials.token
            user.connected = True
            user.save()
        print("Successfully logged in.")
    except Exception as e:
        print(f"An error occurred during login: {e}")

def logout():
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)
        user = AccountDB.objects.filter(platform="YouTube").first()
        if user:
            user.token = ""
            user.connected = False
            user.save()
        print("Successfully logged out.")
    else:
        print("No user is currently logged in.")
