import os
import search_videos
import view_profile
import view_recommended
import view_subscriptions
import video_details
import channel_details
import playlist_items
import video_comments
import auth

def is_logged_in():
    return os.path.exists('token.pickle')

def main():
    while True:
        print("\n1. Log In")
        print("2. Log Out")
        print("3. Search Videos")
        print("4. View Profile Information")
        print("5. View Recommended Videos")
        print("6. View Subscribed Channels")
        print("7. Get Video Details")
        print("8. Get Channel Details")
        print("9. Get Playlist Items")
        print("10. Get Video Comments")
        print("11. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10/11): ")

        if choice == '1':
            auth.login()
        elif choice == '2':
            auth.logout()
        elif choice in {'3', '4', '5', '6', '7', '8', '9', '10'}:
            if not is_logged_in():
                print("You must log in first!")
            else:
                if choice == '3':
                    query = input("Enter search query: ")
                    search_videos.search_videos(query)
                elif choice == '4':
                    view_profile.view_profile()
                elif choice == '5':
                    view_recommended.view_recommended()
                elif choice == '6':
                    sub_choice = input("Enter 'a' to view all subscriptions or 's' to search for a specific subscription: ")
                    if sub_choice.lower() == 'a':
                        view_subscriptions.view_all_subscriptions()
                    elif sub_choice.lower() == 's':
                        query = input("Enter the search query: ")
                        view_subscriptions.search_subscriptions(query)
                    else:
                        print("Invalid choice!")
                elif choice == '7':
                    video_id = input("Enter video ID: ")
                    video_details.get_video_details(video_id)
                elif choice == '8':
                    channel_id = input("Enter channel ID: ")
                    channel_details.get_channel_details(channel_id)
                elif choice == '9':
                    playlist_id = input("Enter playlist ID: ")
                    try:
                        playlist_items.get_playlist_items(playlist_id)
                    except Exception:
                        print("Returning to the main menu...")
                elif choice == '10':
                    video_id = input("Enter video ID: ")
                    video_comments.get_video_comments(video_id)
        elif choice == '11':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 11.")

if __name__ == '__main__':
    main()
