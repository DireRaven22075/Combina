from auth import get_authenticated_service

def search_videos(query):
    youtube = get_authenticated_service()
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=5
    )
    response = request.execute()
    results = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        iframe = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        results.append(f"Title: {title}\nVideo ID: {video_id}\nEmbed: {iframe}\n")
    return results

if __name__ == '__main__':
    search_videos('Python programming')
