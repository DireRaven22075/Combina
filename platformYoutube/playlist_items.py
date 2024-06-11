from auth import get_authenticated_service

def get_playlist_items(playlist_id):
    youtube = get_authenticated_service()
    try:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50  # Adjust as needed
        )
        response = request.execute()
        if not response['items']:
            raise ValueError("No items found in this playlist.")
        for item in response['items']:
            title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            print(f"Title: {title}")
            print(f"Video ID: {video_id}\n")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == '__main__':
    playlist_id = input("Enter playlist ID: ")
    get_playlist_items(playlist_id)
