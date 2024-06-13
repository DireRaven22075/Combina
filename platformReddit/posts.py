import requests

def get_profile_info(headers):
    response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    profile = response.json()
    profile_id = profile['id']
    profile_name = profile['name']
    profile_picture = profile['icon_img']

    return profile_id, profile_name, profile_picture

def get_random_subscribed_posts(headers, limit=5):
    response = requests.get('https://oauth.reddit.com/subreddits/mine/subscriber', headers=headers)
    subscribed_subreddits = response.json()['data']['children']
    posts_info = []

    for subreddit in subscribed_subreddits:
        subreddit_name = subreddit['data']['display_name']
        subreddit_image = subreddit['data']['icon_img']

        response = requests.get(f'https://oauth.reddit.com/r/{subreddit_name}/hot', headers=headers, params={'limit': limit})
        posts = response.json()['data']['children']

        for post in posts:
            post_data = post['data']
            post_info = {
                'subreddit_name': subreddit_name,
                'subreddit_image': subreddit_image,
                'writer_name': post_data['author'],
                'post_title': post_data['title'],
                'post_text': post_data['selftext'],
                'post_image': post_data['url'] if post_data['url'].endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')) else None,
                'post_date': post_data['created_utc'],
                'votes': post_data['score']
            }
            posts_info.append(post_info)
    
    return posts_info

def search_posts(headers, query, subreddit_name='', limit=5):
    if subreddit_name:
        url = f'https://oauth.reddit.com/r/{subreddit_name}/search'
    else:
        url = 'https://oauth.reddit.com/search'

    params = {'q': query, 'limit': limit, 'restrict_sr': 'on' if subreddit_name else 'off'}
    response = requests.get(url, headers=headers, params=params)
    posts = response.json()['data']['children']
    
    results = []
    for post in posts:
        post_data = post['data']
        post_info = {
            'subreddit_name': post_data['subreddit'],
            'subreddit_image': None,  # API does not return subreddit image in search
            'writer_name': post_data['author'],
            'post_title': post_data['title'],
            'post_text': post_data['selftext'],
            'post_image': post_data['url'] if post_data['url'].endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')) else None,
            'post_date': post_data['created_utc'],
            'votes': post_data['score']
        }
        results.append(post_info)
    
    return results
