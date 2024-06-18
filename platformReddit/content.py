from page.models import AccountDB, ContentDB, FileDB
from django.db.models import Max  # Add this import
import praw
from .config import CLIENT_ID, CLIENT_SECRET, USER_AGENT

MAX_POSTS = 10

def get_media_urls(submission):
    media_urls = []
    if hasattr(submission, 'media_metadata'):
        # 이미지 여럿일 경우
        for item in submission.media_metadata.values():
            if 's' in item:
                media_urls.append(item['s']['u'])
    elif hasattr(submission, 'preview'):
        # 이미지 하나인 경우
        for image in submission.preview.get('images', []):
            media_urls.append(image['source']['url'])
    return media_urls




def Content(reddit): #get-content

    user = reddit.user.me()
    print("content in ",user.name)
    print(user)
    if reddit:
        try:
            recommended_posts = []
            for subreddit in reddit.user.subreddits(limit=None):
                for submission in reddit.subreddit(subreddit.display_name).hot(limit=MAX_POSTS):
                    recommended_posts.append(submission)
            # 포스트 하나당
            for idx, submission in enumerate(recommended_posts[:MAX_POSTS], start=1):
                #date = datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d")
                print(f'{idx}. Title: {submission.title}')
                print(f'   Author: {submission.author.name}')
                print(f'   Text: {submission.selftext}')
                print(f'   Url: {submission.url}')
                latest = FileDB.objects.aggregate(max_uid=Max('uid'))['max_uid']
                if latest is None:
                    latest = 0  # 최신 값이 없으면 0으로 초기화

                image_uid = 0
            
                media_urls = get_media_urls(submission)

                for image_url in media_urls:
                    print(f'   Image: {image_url}')
                    image_uid = latest + 1
                    FileDB.objects.create(
                        uid = image_uid,
                        url = image_url
                    ).save()
                    
                ContentDB.objects.create(
                    platform = 'Reddit',
                    userID = submission.author.name,
                    text = submission.title+"|||"+submission.selftext,
                    image_url = image_uid,
                    userIcon = submission.author.icon_img,
                    vote = submission.score,
                ).save()
        except Exception as e:
            print(f'Error fetching posts: {e}')
            return False
    else:
        print('You are not logged in.')
        return False
        