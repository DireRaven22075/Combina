import requests

def view_recommended(headers, limit=5):
    """ Fetches recommended videos from YouTube """
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/videos',
        headers=headers,
        params={
            'part': 'snippet,contentDetails,statistics',
            'chart': 'mostPopular',
            'maxResults': limit
        }
    )
    return response.json()
