import keyring

SERVICE_NAME = 'RedditApp'

def save_credentials(username, token):
    keyring.set_password(SERVICE_NAME, 'username', username)
    keyring.set_password(SERVICE_NAME, 'token', token)

def get_credentials():
    username = keyring.get_password(SERVICE_NAME, 'username')
    token = keyring.get_password(SERVICE_NAME, 'token')
    return username, token

def logout():
    keyring.delete_password(SERVICE_NAME, 'username')
    keyring.delete_password(SERVICE_NAME, 'token')
