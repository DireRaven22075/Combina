from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page.models import ContentDB, FileDB
from .utils import sleep, quit_driver_forcefully
from .account import Account
from django.db.models import Count, Max

MAX_POSTS = 5

class Content:
    #DB에 값만 저장
    @staticmethod
    def free_field(driver):
        try:
            free_field_box = driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a")
            free_field_box.click()
            sleep()
            
            for i in range(1, MAX_POSTS):
                post = driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
                info = driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
                
            
                post_title = post.find_element(By.CLASS_NAME, 'medium').text
                post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                
                print(f"title : {post_title}")
                print(f"text : {post_text}")

                
                post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                
                
                print(f"username : {post_user}")
                # comment 제외
                try:
                    post_vote = info.find_element(By.CLASS_NAME, "vote").text
                    print(f"vote : {post_vote}")
                except:
                    post_vote = 0
                    print("no vote")
                image_url = 0

                try:
                    image_list = []
                    #이미지 uid 이용해서 contentDB's image_url, FileDB's uid uid 값 주고 FileDB url 에 이미지 url 저장
                    post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
                    print(f"image : {post_image}")
                    image_list.append(post_image.split("\"")[1])
                    
                    
                    
                    latest = FileDB.objects.aggregate(max_uid=Max('uid'))['max_uid']
                    if latest is None:
                        latest = 0  # 최신 값이 없으면 0으로 초기화
                    image = None
                    if image_list:
                        for i, image in enumerate(image_list, start=1):
                            print("image exist", image)
                            image_url = latest + 1

                            # # 이미지가 존재하는지 확인
                            # if not FileDB.objects.filter(url=image).exists():
                            #     # 이미지가 존재하지 않는 경우에만 저장
                            FileDB.objects.create(
                                uid=image_url,
                                url=image,
                            ).save()

                except NoSuchElementException:
                    image_url = 0
                    print("no image")
                ContentDB.objects.create(
                    platform = "everytime",
                    userID = post_user,
                    text = post_title+"|||" + post_text,
                    image_url = image_url,
                    vote = post_vote,
                ).save()       
                
        except Exception as e:
            print("free_field error", e)
            return False
        finally:
            print("free_field done")
            #quit_driver_forcefully(driver)
            driver.close()
            print("driver quit forcefully in free_field")
            return True
            



    @staticmethod
    def search_field(search, driver):
        try:
            
            free_field_box = driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a")
            free_field_box.click()
            sleep()

            search_box = driver.find_element(By.NAME, "keyword")
            search_box.send_keys(search)
            search_box.send_keys(Keys.RETURN)
            sleep()

    
            for i in range(1, MAX_POSTS):
                post = driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
                info = driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
              
                post_title = post.find_element(By.CLASS_NAME, 'medium').text
                post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                
                print(f"title : {post_title}")
                print(f"text : {post_text}")

                
                post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                
                
                print(f"username : {post_user}")
                # comment 제외
                try:
                    post_vote = info.find_element(By.CLASS_NAME, "vote").text
                    print(f"vote : {post_vote}")
                except:
                    post_vote = 0
                    print("no vote")

                image_url = 0
                try:
                    image_list = []
                    #이미지 uid 이용해서 contentDB's image_url, FileDB's uid uid 값 주고 FileDB url 에 이미지 url 저장
                    post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
                    image_list.append(post_image.split("\"")[1])

                    print(f"image url : {image_list}") ## 여기까지는 됨
                    # 가장 최신 file의 uid 가져오기

                    file_count = FileDB.objects.aggregate(count=Count('uid'))['count']

                    if file_count > 0:
                        latest = FileDB.objects.latest('uid')
                        print(f"latest : {type(latest)}")
                    else:
                        latest = 0

                    if image_list:
                        for i, image in enumerate(image_list, start=1):
                            print("image exist", image)
                            if latest == 0:
                                image_url = 1
                            else:
                                image_url = latest.uid + 1

                            # # 이미지가 존재하는지 확인
                            # if not FileDB.objects.filter(url=image).exists():
                            #     # 이미지가 존재하지 않는 경우에만 저장
                                FileDB.objects.create(
                                    uid=image_url,
                                    url=image,
                                ).save()
                        
                        
                except NoSuchElementException:    
                    image_url = 0
                    print("no image")

                ContentDB.objects.create(
                    platform = "everytime",
                    userID = post_user,
                    text = post_title+"|||" + post_text,
                    image_url = image_url,
                    vote = post_vote,
                ).save()

        except Exception as e:
            print("search_field error", e)
            return False
        finally:
            print("search_field done")
            #quit_driver_forcefully(driver)
            driver.close()
            print("driver quit forcefully in search_field")
            return True
                