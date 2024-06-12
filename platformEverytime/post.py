from django.shortcuts import render
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from page.models import ContentDB, FileDB
from .account import Account
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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



class Post(Account):

    def __init__(self, request):
        super().__init__(request)

    def post(self, title,text, images=None):
        if self.driver is None:
            print("driver is None in start")
            self.driver = Account.initialize_driver()
            self.driver = self.login()

        try:

            free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a")
            free_field_box.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"writeArticleButton\"]"))
            )
           
           # 글쓰기 //*[@id="writeArticleButton"] 
            post_box = self.driver.find_element(By.XPATH, "//*[@id=\"writeArticleButton\"]")
            post_box.click()
            sleep()
            
           
            title_box = self.driver.find_element(By.NAME, "title")
            title_box.send_keys(title)
            

            text_box = self.driver.find_element(By.NAME, "text")
            text_box.send_keys(text)
            print("text sent")
            set_anonym = self.driver.find_element(By.CLASS_NAME, "anonym")
            set_anonym.click()
            sleep()


            if images is not None:

                image_box = self.driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[2]")
                image_box.click()

                #이미지 업로드
                for image in images:
                    print("image uploading", image)
                    upload_file_from_in_memory(self.driver, image, "input[type=\"file\"]")
                    sleep() 
            
            #에타 포스팅 함부로 주석처리 해제하지 말 것
            #submit_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[3]").click()

        except Exception as e:
            print("post error", e)
            return False
        finally:
           
            print("driver quit in post_field")
            return True