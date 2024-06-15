import requests
CLIENT_ID = 'a-TpD_hJiCllSc7JG3seaA'
CLIENT_SECRET = 'grifUSnHoHW5n8Y-bATjE3DsQmNoTg'
USER_AGENT = 'Combina-webengine_v1.0'
class PlatformReddit:
    def init(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = 'http://localhost:8000/home'
        self.user_agent = USER_AGENT
        self.access_token = None
        self.refresh_token = None

    def authenticate(self, code):
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        post_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        headers = {'User-Agent': self.user_agent}
        response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=post_data, headers=headers)
        token_json = response.json()
        self.access_token = token_json.get('access_token')
        self.refresh_token = token_json.get('refresh_token')
        return self.access_token, self.refresh_token

    def get_profile_info(self):
        if not self.access_token:
            raise Exception('Not authenticated')
        headers = {'Authorization': f'bearer {self.access_token}', 'User-Agent': self.user_agent}
        response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
        return response.json()