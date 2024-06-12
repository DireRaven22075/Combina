from auth import get_authenticated_service

def view_profile():
    youtube = get_authenticated_service()
    request = youtube.channels().list(
        part='snippet',
        mine=True
    )
    response = request.execute()
    profile = []
    for item in response['items']:
        title = item['snippet']['title']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']
        profile.append(f"Name: {title}\nProfile Picture: {thumbnail_url}\n")
    return profile

if __name__ == '__main__':
    view_profile()
