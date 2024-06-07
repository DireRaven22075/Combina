from auth import get_authenticated_service

def view_profile():
    youtube = get_authenticated_service()
    request = youtube.channels().list(
        part='snippet',
        mine=True
    )
    response = request.execute()
    for item in response['items']:
        print(f"Name: {item['snippet']['title']}")
        print(f"Profile Picture: {item['snippet']['thumbnails']['default']['url']}\n")

if __name__ == '__main__':
    view_profile()
