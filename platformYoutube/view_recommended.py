from auth import get_authenticated_service

def view_recommended():
    youtube = get_authenticated_service()
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode='US',  # You can change the region code as needed
        maxResults=5
    )
    response = request.execute()
    for item in response['items']:
        video_id = item['id']
        title = item['snippet']['title']
        iframe = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
        print(f"Title: {title}")
        print(f"Video ID: {video_id}")
        print(f"Embed: {iframe}\n")

if __name__ == '__main__':
    view_recommended()
