from auth import get_authenticated_service

def get_channel_details(channel_id):
    youtube = get_authenticated_service()
    request = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    )
    response = request.execute()
    details = []
    for item in response['items']:
        title = item['snippet']['title']
        subscribers = item['statistics']['subscriberCount']
        views = item['statistics']['viewCount']
        details.append(f"Channel Title: {title}\nSubscribers: {subscribers}\nViews: {views}\n")
    return details

if __name__ == '__main__':
    channel_id = input("Enter channel ID: ")
    get_channel_details(channel_id)
