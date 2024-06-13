def get_profile_info(reddit):
    profile = reddit.user.me()
    profile_id = profile.id
    profile_name = profile.name
    profile_picture = profile.icon_img

    return profile_id, profile_name, profile_picture

def get_saved_posts(reddit, limit=5):
    saved_posts = reddit.user.me().saved(limit=limit)
    return [{
        'title': post.title if hasattr(post, 'title') else 'No title',
        'url': post.url if hasattr(post, 'url') else 'No URL'
    } for post in saved_posts]

def get_upvoted_posts(reddit, limit=5):
    upvoted_posts = reddit.user.me().upvoted(limit=limit)
    return [{
        'title': post.title if hasattr(post, 'title') else 'No title',
        'url': post.url if hasattr(post, 'url') else 'No URL'
    } for post in upvoted_posts]
