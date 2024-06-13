import requests

def search_videos(headers, query):
    """ Searches for videos on YouTube based on a query """
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/search',
        headers=headers,
        params={
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 5
        }
    )
    return response.json()
