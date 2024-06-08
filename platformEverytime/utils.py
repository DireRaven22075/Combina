# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.sessions.models import Session
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import UnexpectedAlertPresentException
# import time
# import random
# import threading


# def sleep(a = 1, b= 1.5):
#     time.sleep(random.uniform(a, b))

# MAX_GET_POST = 3


# class driver_set:
    
#     def __init__(self,request):
#         self.request = request
#         self.id = request.session.get('id', None)
#         self.password = request.session.get('password', None)
#         self.name = request.session.get('name', None)
#         self.driver = self.initialize_driver()
        

#     def initialize_driver(self):
#         options = webdriver.ChromeOptions()
#         #options.add_argument("--headless")
#         options.add_argument("--log-level=3")
#         options.add_argument("--profile-default-content-settings.cookies=1")
#         options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
#         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#         return driver
    
#     @staticmethod
#     def session_is_exist(self):
#         session_key = self.request.session.session_key
#         session = Session.objects.get(session_key=session_key)
#         if session is not None:
#             return True
#         return False
#     @staticmethod
#     def close_driver(self):
#         self.driver.quit()
#         del self.request.session
#         self.request.session.save()
#         print("driver closed")
#     @staticmethod    
#     def login(self):
#         print("login start")
#         session_key = self.request.session.session_key

#         if not session_key:
#             self.request.session.create()
#             session_key = self.request.session.session_key
#             print("create new session")
#             #세션 남아있으면(로그인 되어있으면)
            
           
           
#         try:
#             print("browser is opeening in except")
#             self.driver.get("https://account.everytime.kr/login")
            
#             id_box = self.driver.find_element(By.NAME, "id")
#             id_box.send_keys(self.id)
#             pw_box = self.driver.find_element(By.NAME, "password")
#             pw_box.send_keys(self.password)
#             sumbit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
#             sleep()
#             sumbit_box.click()
#             sleep()
#             cookies = self.driver.get_cookies()
#             if not cookies:
#                 print("login failed")
#                 return None
#             self.name = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]').text
#             print(f"nickname : {self.name}")
            
#             self.request.session['id'] = self.id
#             self.request.session['password'] = self.password
#             self.request.session['name'] = self.name
            
#             self.request.session.save()
#             #print(f"add sessioin : {self.request.session['id'], self.request.session['password']}")
#             print("new session!")
#             return cookies
        
#         except UnexpectedAlertPresentException:
#             print("login failed, try again")
#             self.driver.quit()
#             return None
#     @staticmethod
#     def search_field(self, search, post_count = MAX_GET_POST):
        
#         if search is not None:
#             # 에브리 타임 로그인
#             self.driver.get("https://account.everytime.kr/login")
            
#             id_box = self.driver.find_element(By.NAME, "id")
#             id_box.send_keys(self.id)
#             pw_box = self.driver.find_element(By.NAME, "password")
#             pw_box.send_keys(self.password)
#             sumbit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
#             sleep()
#             sumbit_box.click()
#             cookies = self.driver.get_cookies()
#             if not cookies:
#                 return None
#             sleep()
            
#             # //*[@id="submenu"]/div/div[2]/ul/li[1]/a
#             # //*[@id="container"]/div[4]/div[1]/div/h3/a
#             free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a")
#             free_field_box.click()
#             sleep()
#             search_box = self.driver.find_element(By.NAME, "keyword")
#             search_box.send_keys(search)
#             search_box.send_keys(Keys.RETURN)
#             sleep()

#             post_list = []
        
#             # 10 초 이상 못 가져오면 종료
#             def quit_driver():
#                 self.driver.quit()

#             timer = threading.Timer(10.0, quit_driver)
#             timer.start()


#             for i in range(1, post_count+1):
#                 post = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
#                 info = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
#                 try:
#                     post_title = post.find_element(By.CLASS_NAME, 'medium').text
#                     post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                    
#                     print(f"title : {post_title}")
#                     print(f"text : {post_text}")

                    
#                     post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                    
                    
#                     print(f"username : {post_user}")
#                     # comment 제외
#                     try:
#                         post_vote = info.find_element(By.CLASS_NAME, "vote").text
#                         print(f"vote : {post_vote}")
#                     except:
#                         post_vote = 0
#                         print("no vote")
#                     try:
#                         #이미지 uid 이용해서 contentDB's image_url, FileDB's uid uid 값 주고 FileDB url 에 이미지 url 저장
#                         post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
#                         print(f"image : {post_image}")
#                         image_url = post_image.split("\"")[1]
#                         print(f"image url : {image_url}")
#                         # background-image: url("https://cf-ea.everytime.kr/attach_thumbnail/924/67853365/everytime-1717585771365.jpg?Expires=1717675473&Key-Pair-Id=APKAICU6XZKH23IGASFA&Signature=sTisCXoMGvqczsTMKk17v1Eq32ZDo2ccCLxoWNek88yG-Ib7O0jY9EEj3HVaY9s-mocdfqkRkWeXGBNbCfHhcIqPUbRkv2w~5-dpnY5ojPgX4R4BTIIVl0X~AFicxN0y9ugFfbik7JF5c4VnevB8wejzjq33jLR7cTGTDIYl1aBmfHjYXBqzdBMaST3x3DWltcLJZYGHga4tsatFH7TnZVtDIVrF8hrlAKl0nv5GoD~Ev-wq~AI4tvKqQPQXV03H53ss-3gl-adQ2orOJpt58566TvXH0ZS2q0544bIJ5sDlnpbKQT7bV3uQnKm2XUoJsC9xdGDSXaxuigS~L-eYpw__");
#                     except:
#                         image_url = None
#                         print("no image")
#                 except:
#                     print("failed")
#                 post_list.append({"title":post_title, "text":post_text, "username":post_user,"vote":post_vote, "image":image_url})
#             self.driver.quit()
#             return post_list
#         else:
#             self.driver.quit()
#             return None
#     @staticmethod
#     def image_field(self, post_count = MAX_GET_POST):
       
#         #print(f"session in free_field: {self.request.session['id'], self.request.session['password'], self.request.session['name']}")
#         self.driver.get("https://account.everytime.kr/login")
            
#         id_box = self.driver.find_element(By.NAME, "id")
#         id_box.send_keys(self.id)
#         pw_box = self.driver.find_element(By.NAME, "password")
#         pw_box.send_keys(self.password)
#         sumbit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
#         sleep()
#         sumbit_box.click()
#         cookies = self.driver.get_cookies()
#         if not cookies:
#             return None
        
#         sleep()
#         free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[11]/ul/li[2]/a")
#         free_field_box.click()
#         sleep()
#         post_list = []
        
#         # 10 초 이상 못 가져오면 끝
#         def quit_driver():
#             self.driver.quit()

#         timer = threading.Timer(10.0, quit_driver)
#         timer.start()


#         for i in range(1, post_count+1):
#             post = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
#             info = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
#             try:
#                 post_title = post.find_element(By.CLASS_NAME, 'medium').text
#                 post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                
#                 print(f"title : {post_title}")
#                 print(f"text : {post_text}")

                
#                 post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                
                
#                 print(f"username : {post_user}")
#                 # comment 제외
#                 try:
#                     post_vote = info.find_element(By.CLASS_NAME, "vote").text
#                     print(f"vote : {post_vote}")
#                 except:
#                     post_vote = 0
#                     print("no vote")
#                 try:
#                     #이미지 uid 이용해서 contentDB's image_url, FileDB's uid uid 값 주고 FileDB url 에 이미지 url 저장
#                     post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
#                     print(f"image : {post_image}")
#                     image_url = post_image.split("\"")[1]
#                     print(f"image url : {image_url}")
#                     # background-image: url("https://cf-ea.everytime.kr/attach_thumbnail/924/67853365/everytime-1717585771365.jpg?Expires=1717675473&Key-Pair-Id=APKAICU6XZKH23IGASFA&Signature=sTisCXoMGvqczsTMKk17v1Eq32ZDo2ccCLxoWNek88yG-Ib7O0jY9EEj3HVaY9s-mocdfqkRkWeXGBNbCfHhcIqPUbRkv2w~5-dpnY5ojPgX4R4BTIIVl0X~AFicxN0y9ugFfbik7JF5c4VnevB8wejzjq33jLR7cTGTDIYl1aBmfHjYXBqzdBMaST3x3DWltcLJZYGHga4tsatFH7TnZVtDIVrF8hrlAKl0nv5GoD~Ev-wq~AI4tvKqQPQXV03H53ss-3gl-adQ2orOJpt58566TvXH0ZS2q0544bIJ5sDlnpbKQT7bV3uQnKm2XUoJsC9xdGDSXaxuigS~L-eYpw__");
#                 except:
#                     image_url = None
#                     print("no image")
#             except:
#                 print("failed")
            
#             post_list.append({"title":post_title, "text":post_text, "username":post_user,"vote":post_vote, "image":image_url})
#         self.driver.quit()
#         return post_list
    

#     # 자유 게시판 검색
#     @staticmethod
#     def free_field(self, post_count = MAX_GET_POST):

#         #print(f"session in free_field: {self.request.session['id'], self.request.session['password'], self.request.session['name']}")
#         self.driver.get("https://account.everytime.kr/login")
            
#         id_box = self.driver.find_element(By.NAME, "id")
#         id_box.send_keys(self.id)
#         pw_box = self.driver.find_element(By.NAME, "password")
#         pw_box.send_keys(self.password)
#         sumbit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
#         sleep()
#         sumbit_box.click()
#         cookies = self.driver.get_cookies()
#         if not cookies:
#             return None
        
#         sleep()
#         free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[4]/div[1]/div/h3/a")
#         free_field_box.click()
#         sleep()
#         post_list = []
        
#         # 10 초 이상 못 가져오면 종료
#         def quit_driver():
#             self.driver.quit()

#         timer = threading.Timer(10.0, quit_driver)
#         timer.start()

#         for i in range(1, post_count+1):
#             post = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
#             info = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
#             try:
#                 post_title = post.find_element(By.CLASS_NAME, 'medium').text
#                 post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                
#                 print(f"title : {post_title}")
#                 print(f"text : {post_text}")

                
#                 post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                
                
#                 print(f"username : {post_user}")
#                 # comment 제외
#                 try:
#                     post_vote = info.find_element(By.CLASS_NAME, "vote").text
#                     print(f"vote : {post_vote}")
#                 except:
#                     post_vote = 0
#                     print("no vote")

#                 try:
#                     #이미지 uid 이용해서 contentDB's image_url, FileDB's uid uid 값 주고 FileDB url 에 이미지 url 저장
#                     post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
#                     print(f"image : {post_image}")
#                     image_url = post_image.split("\"")[1]
#                     print(f"image url : {image_url}")
#                 except:    
#                     image_url = None
#                     print("no image")
#             except:
#                 print("failed")
#             post_list.append({"title":post_title, "text":post_text, "username":post_user,"vote":post_vote, "image":image_url})
#         self.driver.quit()
#         return post_list
#     @staticmethod
#     def post(self, text, image):
#         self.driver.get("https://account.everytime.kr/login")

#         self.driver.get("https://account.everytime.kr/login")
            
#         id_box = self.driver.find_element(By.NAME, "id")
#         id_box.send_keys(self.id)
#         pw_box = self.driver.find_element(By.NAME, "password")
#         pw_box.send_keys(self.password)
#         sumbit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
#         sleep()
#         sumbit_box.click()
#         cookies = self.driver.get_cookies()
#         if not cookies:
#             return None
        
#         sleep()
#         free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[4]/div[1]/div/h3/a")
#         free_field_box.click()
#         sleep()

#         post_box = self.driver.find_element(By.XPATH, "//*[@id=\"writeArticleButton\"]")
#         post_box.click()
#         sleep()
#         title = text.split("\n")[0]
#         title_box = self.driver.find_element(By.NAME, "title")
#         title_box.send_keys(title)

#         text_box = self.driver.find_element(By.NAME, "text")
#         text_box.send_keys(text)
#         sleep()

#         image_box = self.driver.find_element(By.NAME, "image")
#         image_box.send_keys(image)
#         #post 보내기
#         #post_box.send_keys(Keys.RETURN)
#         post = {"title":title, "text":text, "username":self.name,"vote":0, "image":None}
#         return post
        

