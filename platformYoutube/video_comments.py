from auth import get_authenticated_service

def get_video_comments(video_id):
    youtube = get_authenticated_service()
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=50  # Adjust as needed
    )
    response = request.execute()
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comments.append(f"Author: {author}\nComment: {comment}\n")
    return comments

if __name__ == '__main__':
    video_id = input("Enter video ID: ")
    get_video_comments(video_id)
