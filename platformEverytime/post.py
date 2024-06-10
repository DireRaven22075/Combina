from django.shortcuts import render
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from page.models import ContentDB, FileDB
from .account import Account
from .utils import sleep, quit_driver_forcefully
import tempfile
import os

def upload_file_from_in_memory(driver, in_memory_file, upload_input_selector):
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        # InMemoryUploadedFile의 데이터를 임시 파일에 씀
        for chunk in in_memory_file.chunks():
            tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    try:
        # <input type="file"> 요소에 파일 경로를 설정
        file_input = driver.find_element(By.CSS_SELECTOR, upload_input_selector)
        file_input.send_keys(tmp_file_path)
        print(f"Image uploaded: {tmp_file_path}")
    finally:
        # 임시 파일 삭제
        os.remove(tmp_file_path)
        print(f"Temporary file deleted: {tmp_file_path}")



class Post:
    @staticmethod
    def post(text, images=None, driver=None):
        
        try:

            free_field_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[4]/div[1]/div/h3/a")
            free_field_box.click()
            sleep()
            
           # 글쓰기 //*[@id="writeArticleButton"] 
            post_box = driver.find_element(By.XPATH, "//*[@id=\"writeArticleButton\"]")
            post_box.click()
            sleep()
            title = text.split("\n")[0]
            text_split = text.split("\n")[1]
           
            title_box = driver.find_element(By.NAME, "title")
            title_box.send_keys(title)
            

            text_box = driver.find_element(By.NAME, "text")
            text_box.send_keys(text_split)
            print("text sent")
            set_anonym = driver.find_element(By.CLASS_NAME, "anonym")
            set_anonym.click()
            sleep()


            if images is not None:

                image_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[2]")
                image_box.click()

                #이미지 업로드
                for image in images:
                    print("image uploading", image)
                    upload_file_from_in_memory(driver, image, "input[type=\"file\"]")
                    sleep() 
            
            #에타 포스팅 함부로 주석처리 해제하지 말 것
            #submit_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[3]").click()

        except Exception as e:
            print("post error", e)
            return False
        finally:
            quit_driver_forcefully(driver)
            print("driver quit in post_field")
            return True