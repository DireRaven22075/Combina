import requests
def get_facebook_login_token(app_id, app_secret, redirect_uri):
    # Make a GET request to the Facebook API to obtain the login token
    response = requests.get(f"https://graph.facebook.com/v13.0/oauth/access_token?client_id={app_id}&client_secret={app_secret}&redirect_uri={redirect_uri}&grant_type=client_credentials")
    # Parse the response JSON and extract the login token
    token_data = response.json()
    login_token = token_data.get("access_token")
    return login_token
# Replace the placeholders with your own app ID, app secret, and redirect URI
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"
# Call the function to get the Facebook login token
login_token = get_facebook_login_token(app_id, app_secret, redirect_uri)
# Print the login token
print(login_token)