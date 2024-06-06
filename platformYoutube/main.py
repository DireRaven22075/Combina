import search_videos
import view_profile
import view_recommended
import view_subscriptions
import video_details
import channel_details
import playlist_items
import video_comments

def main():
    while True:
        print("\n1. Search Videos")
        print("2. View Profile Information")
        print("3. View Recommended Videos")
        print("4. View Subscribed Channels")
        print("5. Get Video Details")
        print("6. Get Channel Details")
        print("7. Get Playlist Items")
        print("8. Get Video Comments")
        print("9. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6/7/8/9): ")

        if choice == '1':
            query = input("Enter search query: ")
            search_videos.search_videos(query)
        elif choice == '2':
            view_profile.view_profile()
        elif choice == '3':
            view_recommended.view_recommended()
        elif choice == '4':
            sub_choice = input("Enter 'a' to view all subscriptions or 's' to search for a specific subscription: ")
            if sub_choice.lower() == 'a':
                view_subscriptions.view_all_subscriptions()
            elif sub_choice.lower() == 's':
                query = input("Enter the search query: ")
                view_subscriptions.search_subscriptions(query)
            else:
                print("Invalid choice!")
        elif choice == '5':
            video_id = input("Enter video ID: ")
            video_details.get_video_details(video_id)
        elif choice == '6':
            channel_id = input("Enter channel ID: ")
            channel_details.get_channel_details(channel_id)
        elif choice == '7':
            playlist_id = input("Enter playlist ID: ")
            try:
                playlist_items.get_playlist_items(playlist_id)
            except Exception:
                print("Returning to the main menu...")
        elif choice == '8':
            video_id = input("Enter video ID: ")
            video_comments.get_video_comments(video_id)
        elif choice == '9':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 9.")

if __name__ == '__main__':
    main()
