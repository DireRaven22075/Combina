# platformReddit/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from page.models import *
import praw
import json
import os
from datetime import datetime

class RedditApp:
    def __init__(self):
        self.client_id = 'a-TpD_hJiCllSc7JG3seaA'
        self.client_secret = 'grifUSnHoHW5n8Y-bATjE3DsQmNoTg'
        self.user_agent = 'Combina-webengine_v1.0'
        self.credentials_file = 'credentials.json'
        self.reddit = None
        self.username = None
        self.load_credentials()

    def save_credentials(self, username, password): #보류
        credentials = {
            'username': username,
            'password': password
        }
        with open(self.credentials_file, 'w') as f:
            json.dump(credentials, f)

    def load_credentials(self): #보류
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                credentials = json.load(f)
                self.auto_login(credentials['username'], credentials['password'])

    def auto_login(self, username, password): #보류
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent=self.user_agent,
                                  username=username,
                                  password=password)
        try:
            user = self.reddit.user.me()
            self.username = user.name
            print(f'Automatically logged in as {self.username}')
        except Exception as e:
            print(f'Failed to auto login: {e}')
            self.reddit = None

    def login(self, request): #connect
        if (request.method == 'POST'):
            name = request.POST.get('name')
            password = request.POST.get('password')
            self.reddit = praw.Reddit(client_id=self.client_id,
                                    client_secret=self.client_secret,
                                    user_agent=self.user_agent,
                                    username=name,
                                    password=password)
            
            return redirect(request.META.get('HTTP_REFERER'), '/home')
        try:
            user = self.reddit.user.me()
        except Exception as e:
            print(f'Failed to login: {e}')
            self.reddit = None

    def logout(self): #disconnect
        self.reddit = None
        self.username = None
        if os.path.exists(self.credentials_file):
            os.remove(self.credentials_file)
        print('Logged out and credentials removed.')

    def view_profile_info(self): # 프로필 정보 가져와서 model에 저장
        account = AccountDB.objects.filter(platform='Reddit').first()
        if (AccountDB.objects.filter(platform='Reddit').first().connected == True):
            try:
                user = self.reddit.user.me()
                account.name = user.name
                account.icon = user.icon_img
                account.save()
            except Exception as e:
                print(f'Error fetching profile info: {e}')

        if self.reddit:
            try:
                user = self.reddit.user.me()
                print(f'Username: {user.name}')
                print(f'Profile Picture: {user.icon_img}')
            except Exception as e:
                print(f'Error fetching profile info: {e}')
        else:
            print('You are not logged in.')

    def bring_posts(self): #get-content
        if self.reddit:
            try:
                recommended_posts = []
                for subreddit in self.reddit.user.subreddits(limit=None):
                    for submission in self.reddit.subreddit(subreddit.display_name).hot(limit=20):
                        recommended_posts.append(submission)
                for idx, submission in enumerate(recommended_posts[:20], start=1):
                    date = datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d")
                    print(f'{idx}. Title: {submission.title}')
                    print(f'   Author: {submission.author.name}')
                    print(f'   Date: {date}')
                    print(f'   Text: {submission.selftext}')
                    if submission.url:
                        print(f'   URL: {submission.url}')
                    if submission.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
                        print(f'   Image URL: {submission.url}')
                    print('--------------------------')
            except Exception as e:
                print(f'Error fetching posts: {e}')
        else:
            print('You are not logged in.')

    def create_post(self): #post
        if self.reddit:
            try:
                title = input('Enter the title of the post: ')
                content = input('Enter the content of the post: ')
                user = self.reddit.user.me()
                submission = self.reddit.subreddit('u_' + user.name).submit(title, selftext=content)
                print(f'Post created: {submission.url}')
            except Exception as e:
                print(f'Error creating post: {e}')
        else:
            print('You are not logged in.')

    def display_menu(self): #test용
        while True:
            print('\nMenu:')
            if self.username:
                print(f'Logged in as: {self.username}')
            print('1. Login')
            print('2. Logout')
            print('3. View profile info')
            print('4. Bring posts')
            print('5. Create posts')
            print('6. Exit')
            choice = input('Enter your choice: ')

            if choice == '1':
                self.login()
            elif choice == '2':
                self.logout()
            elif choice == '3':
                self.view_profile_info()
            elif choice == '4':
                self.bring_posts()
            elif choice == '5':
                self.create_post()
            elif choice == '6':
                print('Exiting...')
                break
            else:
                print('Invalid choice. Please try again.')
