from auth import get_authenticated_service

def view_recommended(max_results=15):
    youtube = get_authenticated_service()
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode='US',  # You can change the region code as needed
        maxResults=max_results
    )
    response = request.execute()
    recommendations = []
    for item in response['items']:
        video_id = item['id']
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnail = item['snippet']['thumbnails']['default']['url']
        channel_title = item['snippet']['channelTitle']
        publish_date = item['snippet']['publishedAt']
        recommendations.append({
            'video_id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'channel_title': channel_title,
            'publish_date': publish_date,
        })
    return recommendations

if __name__ == '__main__':
    view_recommended()
