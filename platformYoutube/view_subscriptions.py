from auth import get_authenticated_service

def list_all_subscriptions(youtube):
    request = youtube.subscriptions().list(
        part='snippet',
        mine=True,
        maxResults=50  # Adjust as needed, max 50 per request
    )
    response = request.execute()
    subscriptions = response['items']
    while 'nextPageToken' in response:
        request = youtube.subscriptions().list(
            part='snippet',
            mine=True,
            maxResults=50,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        subscriptions.extend(response['items'])
    
    return subscriptions

def view_all_subscriptions():
    youtube = get_authenticated_service()
    subscriptions = list_all_subscriptions(youtube)
    results = []
    for item in subscriptions:
        title = item['snippet']['title']
        channel_id = item['snippet']['resourceId']['channelId']
        channel_url = f'https://www.youtube.com/channel/{channel_id}'
        results.append(f"Channel Title: {title}\nChannel URL: {channel_url}\n")
    return results

def search_subscriptions(query):
    youtube = get_authenticated_service()
    subscriptions = list_all_subscriptions(youtube)
    filtered_subscriptions = [item for item in subscriptions if query.lower() in item['snippet']['title'].lower()]
    if filtered_subscriptions:
        results = []
        for item in filtered_subscriptions:
            title = item['snippet']['title']
            channel_id = item['snippet']['resourceId']['channelId']
            channel_url = f'https://www.youtube.com/channel/{channel_id}'
            results.append(f"Channel Title: {title}\nChannel URL: {channel_url}\n")
        return results
    else:
        return [f"No subscriptions found with the query '{query}'"]

if __name__ == '__main__':
    choice = input("Enter 'a' to view all subscriptions or 's' to search for a specific subscription: ")
    if choice.lower() == 'a':
        view_all_subscriptions()
    elif choice.lower() == 's':
        query = input("Enter the search query: ")
        search_subscriptions(query)
    else:
        print("Invalid choice!")
