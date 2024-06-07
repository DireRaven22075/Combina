from auth import get_authenticated_service

def get_channel_details(channel_id):
    youtube = get_authenticated_service()
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    response = request.execute()
    for item in response['items']:
        title = item['snippet']['title']
        subscribers = item['statistics']['subscriberCount']
        views = item['statistics']['viewCount']
        print(f"Channel Title: {title}")
        print(f"Subscribers: {subscribers}")
        print(f"Views: {views}\n")

if __name__ == '__main__':
    channel_id = input("Enter channel ID: ")
    get_channel_details(channel_id)
