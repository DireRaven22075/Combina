from googleapiclient.discovery import build
from .auth import get_authenticated_service
from page.models import ContentDB, FileDB
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def search_recommended_videos(max_results=20):
    try:
        youtube = get_authenticated_service()
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            chart='mostPopular',
            regionCode='US',  # You can adjust the regionCode as needed
            maxResults=max_results
        )
        response = request.execute()
        videos = []

        for item in response['items']:
            video_id = item['id']
            description = item['snippet']['description']
            channel_title = item['snippet']['channelTitle']
            publish_date = item['snippet']['publishedAt']
            channel_id = item['snippet']['channelId']

            # Fetch channel details
            channel_request = youtube.channels().list(
                part='snippet',
                id=channel_id
            )
            channel_response = channel_request.execute()
            channel_info = channel_response['items'][0]['snippet']
            channel_profile_picture = channel_info['thumbnails']['high']['url']

            video_url = f'https://www.youtube.com/watch?v={video_id}'

            data = ContentDB.objects.create()
            data.platform = "Youtube"
            data.userID = channel_title
            data.text = description
            data.image_url = 0
            data.userIcon = channel_profile_picture
            data.save()
            
            file = FileDB.objects.create()
            file.uid = data.id
            file.url = video_url
            file.save()
            data.image_url = data.id
            data.save()
            
            videos.append({
                'video_url': video_url,
                'channel_name': channel_title,
                'channel_profile_picture': channel_profile_picture,
                'description': description,
                'upload_date': publish_date
            })
        
        logger.debug(f"Successfully fetched {len(videos)} videos and saved to database.")
        return videos

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
