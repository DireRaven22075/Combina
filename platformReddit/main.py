from auth import login, logout, save_credentials, get_credentials
from reddit_profile import get_profile_info, get_saved_posts, get_upvoted_posts
from posts import get_posts_info, get_random_subscribed_posts, search_posts
from friends import get_friends_list
import praw

def main():
    client_id = 'a-TpD_hJiCllSc7JG3seaA'
    client_secret = 'grifUSnHoHW5n8Y-bATjE3DsQmNoTg'
    user_agent = 'Combina-Reddit'

    reddit = None

    # Attempt to log in with saved credentials
    username, password = get_credentials()
    if username and password:
        try:
            reddit = login(client_id, client_secret, username, password, user_agent)
        except praw.exceptions.PRAWException as e:
            print(f"Automatic login failed: {e}")
            reddit = None

    # If automatic login fails or no credentials are saved, prompt for login
    if not reddit:
        while not reddit:
            username = input("Enter your Reddit username: ")
            password = input("Enter your Reddit password: ")
            save = input("Do you want to save your credentials for future use? (yes/no): ").strip().lower()
            if save == 'yes':
                save_credentials(username, password)

            try:
                reddit = login(client_id, client_secret, username, password, user_agent)
            except praw.exceptions.PRAWException as e:
                print(f"Authentication failed: {e}")
                print("Please try again.")
                reddit = None

    while True:
        print("\nOptions:")
        print("1. Log in")
        print("2. Log out")
        print("3. Get profile information")
        print("4. Get posts information from a specific subreddit")
        print("5. Get friends list")
        print("6. Get saved posts")
        print("7. Get upvoted posts")
        print("8. Get posts from random subscribed subreddits")
        print("9. Search posts")
        print("10. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            if reddit:
                print("Already logged in.")
            else:
                while not reddit:
                    username = input("Enter your Reddit username: ")
                    password = input("Enter your Reddit password: ")
                    save = input("Do you want to save your credentials for future use? (yes/no): ").strip().lower()
                    if save == 'yes':
                        save_credentials(username, password)

                    try:
                        reddit = login(client_id, client_secret, username, password, user_agent)
                    except praw.exceptions.PRAWException as e:
                        print(f"Authentication failed: {e}")
                        print("Please try again.")
                        reddit = None

        elif choice == '2':
            if reddit:
                logout(reddit)
                reddit = None
            else:
                print("Not logged in.")

        elif choice == '3':
            if reddit:
                profile_id, profile_name, profile_picture = get_profile_info(reddit)
                print(f"Profile ID: {profile_id}")
                print(f"Profile Name: {profile_name}")
                print(f"Profile Picture: {profile_picture}")
            else:
                print("Log in first.")

        elif choice == '4':
            if reddit:
                subreddit_name = input("Enter subreddit name: ")
                posts_info = get_posts_info(reddit, subreddit_name)
                for post in posts_info:
                    print(f"Post Text: {post['text']}")
                    print(f"Post Image: {post['image']}")
                    print(f"Post Comments: {post['comments']}")
                    print(f"Post Votes: {post['votes']}")
                    print(f"Post URL: {post['url']}")
                    print("-----------")
            else:
                print("Log in first.")

        elif choice == '5':
            friends = get_friends_list()
            for friend in friends:
                print(f"Friend Name: {friend['name']}")
                print(f"Profile URL: {friend['profile_url']}")
                print("-----------")

        elif choice == '6':
            if reddit:
                saved_posts = get_saved_posts(reddit)
                for post in saved_posts:
                    print(f"Title: {post['title']}")
                    print(f"URL: {post['url']}")
                    print("-----------")
            else:
                print("Log in first.")

        elif choice == '7':
            if reddit:
                upvoted_posts = get_upvoted_posts(reddit)
                for post in upvoted_posts:
                    print(f"Title: {post['title']}")
                    print(f"URL: {post['url']}")
                    print("-----------")
            else:
                print("Log in first.")

        elif choice == '8':
            if reddit:
                limit_posts = int(input("Enter the number of posts to fetch from each random subreddit: "))
                subscribed_posts = get_random_subscribed_posts(reddit, limit_posts)
                for post in subscribed_posts:
                    print(f"Subreddit: {post['subreddit']}")
                    print(f"Post Text: {post['text']}")
                    print(f"Post Image: {post['image']}")
                    print(f"Post Comments: {post['comments']}")
                    print(f"Post Votes: {post['votes']}")
                    print(f"Post URL: {post['url']}")
                    print("-----------")
            else:
                print("Log in first.")

        elif choice == '9':
            if reddit:
                query = input("Enter search query: ")
                subreddit_name = input("Enter subreddit name (leave blank for all): ")
                search_results = search_posts(reddit, query, subreddit_name)
                for result in search_results:
                    print(f"Subreddit: {result['subreddit']}")
                    print(f"Title: {result['title']}")
                    print(f"Text: {result['text']}")
                    print(f"URL: {result['url']}")
                    print("-----------")
            else:
                print("Log in first.")

        elif choice == '10':
            if reddit:
                logout(reddit)
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
