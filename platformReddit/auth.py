import praw
import keyring

SERVICE_NAME = 'RedditApp'

def save_credentials(username, password):
    keyring.set_password(SERVICE_NAME, 'username', username)
    keyring.set_password(SERVICE_NAME, 'password', password)

def get_credentials():
    username = keyring.get_password(SERVICE_NAME, 'username')
    password = keyring.get_password(SERVICE_NAME, 'password')
    return username, password

def login(client_id, client_secret, username, password, user_agent):
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)
    print(f"Logged in as: {reddit.user.me()}")
    return reddit

def logout(reddit):
    reddit.user.me = None
    print("Logged out.")
