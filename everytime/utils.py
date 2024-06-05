from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
MAX_GET_POST = 3

def sleep(a = 1, b= 1.5):
    time.sleep(random.uniform(a, b))

class driver_set:
    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.options = webdriver.ChromeOptions()
        self.name = ""
    
    def __str__(self):
        return self.name
    def login(self, id, pw):
        if not self.driver.session_id:
            return None
        print("browser is opeening")
        self.options.add_argument("--headless")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        self.driver.get("https://account.everytime.kr/login")
        self.post_list = []
        id_box = self.driver.find_element(By.NAME, "id")
        id_box.send_keys(id)
        pw_box = self.driver.find_element(By.NAME, "password")
        pw_box.send_keys(pw)
        sumbit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
        sumbit_box.click()
        sleep()
        cookies = self.driver.get_cookies()
        self.name = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]').text
        print(f"nickname : {self.name}")
        context = {
            "cookies" : cookies,
            "name" : self.name,
        }
        return context
    
    def search_field(self, post_count = MAX_GET_POST):
        if not self.driver.session_id:
            return None

    # 자유 게시판 검색
    def free_field(self, post_count = MAX_GET_POST):
        if not self.driver.session_id:
            return None
        free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[4]/div[1]/div/h3/a")
        free_field_box.click()
        sleep()
        for i in range(1, post_count+1):
            post = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
            info = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
            try:
                post_title = post.find_element(By.CLASS_NAME, 'medium').text
                post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                sleep()
                print(f"title : {post_title}")
                print(f"text : {post_text}")

                post_date = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/time").text
                post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                sleep()
                print(f"date : {post_date}")
                print(f"username : {post_user}")
                #vote, comment, image 제외
            #     try:
            #         post_vote = info.find_element(By.CLASS_NAME, "vote").text
            #         print(f"vote : {post_vote}")
            #     except:
            #         post_vote = 0
            #         print("no vote")
            #     try:
            #         post_comment = info.find_element(By.CLASS_NAME, "comment").text
            #         print(f"comment : {post_comment}")
            #     except:
            #         post_comment = 0
            #         print("no comment")
            #     try:
            #         post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
            #         print(f"image : {post_image}")
            #         image_url = str(post_image).split("\"")[1]
            #         print(f"image url : {image_url}")
            #     except:
            #         post_image = ""
            #         print("no image")
            except:
                print("failed")
            self.post_list.append({"title":post_title, "text":post_text, "date":post_date, "username":post_user })
                                   #"vote":post_vote, "comment":post_comment, "image":post_image})
        return self.post_list
            
