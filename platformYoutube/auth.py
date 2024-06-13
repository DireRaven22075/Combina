from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build
from page.models import AccountDB

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
TOKEN_PATH = "../temp/token.pickle"  # 절대 경로로 설정

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(credentials, token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

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
