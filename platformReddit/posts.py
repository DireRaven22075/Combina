import random

def get_posts_info(reddit, subreddit_name, limit=5):
    subreddit = reddit.subreddit(subreddit_name)
    posts_info = []
    
    for post in subreddit.hot(limit=limit):
        post_text = post.selftext
        post_image = post.url if post.url.endswith(('.jpg', '.jpeg', '.png')) else None
        post_comments = [comment.body for comment in post.comments.list()[:5]]  # Get top 5 comments
        post_votes = post.score
        post_url = post.url

        post_info = {
            'text': post_text,
            'image': post_image,
            'comments': post_comments,
            'votes': post_votes,
            'url': post_url
        }
        posts_info.append(post_info)
    
    return posts_info

def get_random_subscribed_posts(reddit, limit=5):
    posts_info = []
    try:
        print("Fetching subscribed subreddits...")
        subscribed_subreddits = list(reddit.user.subreddits(limit=None))
        random.shuffle(subscribed_subreddits)
        
        for subreddit in subscribed_subreddits:
            print(f"Fetching posts from subreddit: {subreddit.display_name}")
            for post in subreddit.hot(limit=limit):
                post_text = post.selftext
                post_image = post.url if post.url.endswith(('.jpg', '.jpeg', '.png')) else None
                post_comments = [comment.body for comment in post.comments.list()[:5]]  # Get top  5 comments
                post_votes = post.score
                post_url = post.url

                post_info = {
                    'subreddit': subreddit.display_name,
                    'text': post_text,
                    'image': post_image,
                    'comments': post_comments,
                    'votes': post_votes,
                    'url': post_url
                }
                posts_info.append(post_info)
            if len(posts_info) >= limit:
                break
        print("Finished fetching posts.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return posts_info

def search_posts(reddit, query, subreddit_name='', limit=5):
    if subreddit_name:
        subreddit = reddit.subreddit(subreddit_name)
        search_results = subreddit.search(query, limit=limit, params={'restrict_sr': 'on'})
    else:
        search_results = reddit.subreddit('all').search(query, limit=limit, params={'restrict_sr': 'on'})
    
    results = []
    for post in search_results:
        post_info = {
            'subreddit': post.subreddit.display_name,
            'title': post.title,
            'text': post.selftext,
            'url': post.url
        }
        results.append(post_info)
    
    return results
