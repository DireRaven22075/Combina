import tempfile
import os
import base64
from django.core.files.base import ContentFile

def Post(reddit ,title, text=None, image=None):
  
    if reddit:
        try:

            user = reddit.user.me()
            subreddit_name = 'u_' + user.name
            print("subreddit_name : ", subreddit_name)
            if image:
                print("in image")
     
                # 임시 폴더
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    temp.write(image.read())
                    temp_path = temp.name
                print("temp_path : ", temp_path)
                try: 
                    submission = reddit.subreddit(subreddit_name).submit_image(title, temp_path)
                    
                    print("Post created image : ", submission.url)
                    os.remove(temp_path)
                    return True
                except Exception as e:
                    print("Error creating post image", e)
                    return False
                
            else:
                submission = reddit.subreddit(subreddit_name).submit(title, selftext=text)
                print("Post created", submission.url)
                return True
        except Exception as e:
            print("Error creating post", e)
    else:
        print("login error")


  