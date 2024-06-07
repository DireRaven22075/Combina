from auth import get_authenticated_service

def get_video_details(video_id):
    youtube = get_authenticated_service()
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    )
    response = request.execute()
    for item in response['items']:
        title = item['snippet']['title']
        views = item['statistics']['viewCount']
        likes = item['statistics']['likeCount']
        comments = item['statistics']['commentCount']
        print(f"Title: {title}")
        print(f"Views: {views}")
        print(f"Likes: {likes}")
        print(f"Comments: {comments}\n")

if __name__ == '__main__':
    video_id = input("Enter video ID: ")
    get_video_details(video_id)
