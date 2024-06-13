from .auth import get_authenticated_service

def view_recommended(max_results=15):
    youtube = get_authenticated_service()
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode='US',  # 필요에 따라 지역 코드를 변경할 수 있음
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
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        recommendations.append({
            'video_id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'channel_title': channel_title,
            'publish_date': publish_date,
            'video_url': video_url
        })
    return recommendations

if __name__ == '__main__':
    view_recommended()
