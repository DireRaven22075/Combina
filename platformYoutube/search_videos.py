from platformYoutube.auth import get_authenticated_service  # Corrected import

def search_videos(query, max_results=5):
    youtube = get_authenticated_service()
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()
    results = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnail = item['snippet']['thumbnails']['default']['url']
        channel_title = item['snippet']['channelTitle']
        publish_date = item['snippet']['publishedAt']
        results.append({
            'video_id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'channel_title': channel_title,
            'publish_date': publish_date,
        })
    return results
