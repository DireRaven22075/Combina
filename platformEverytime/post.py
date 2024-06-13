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
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        for chunk in in_memory_file.chunks():
            tmp_file.write(chunk)
        tmp_file_path = tmp_file.name

    try:
        file_input = driver.find_element(By.CSS_SELECTOR, upload_input_selector)
        file_input.send_keys(tmp_file_path)
    finally:
        os.remove(tmp_file_path)



def Post(driver, title, text, images = None):
    try:
        print("post title", title)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a"))
        )
        sleep()

        free_field_box = driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a")
        free_field_box.click()
        driver.refresh()
   
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"writeArticleButton\"]"))
        )
        sleep()
        print("post text", text)
        post_box = driver.find_element(By.XPATH, "//*[@id=\"writeArticleButton\"]")
        post_box.click()
        sleep()
        
        title_box = driver.find_element(By.NAME, "title")
        title_box.send_keys(title)
        print("title sent1")
        text_box = driver.find_element(By.NAME, "text")
        text_box.send_keys(text)
        print("text sent2")
        set_anonym = driver.find_element(By.CLASS_NAME, "anonym")
        set_anonym.click()
        sleep()

        if images is not None:

            image_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[2]")
            image_box.click()

            #이미지 업로드
            for image in images:
                upload_file_from_in_memory(driver, image, "input[type=\"file\"]")
                sleep(3,4) # 이미지 옵션 끄면 업로드 불가
            # 이미지 업로드 비활성화
        #에타 포스팅 함부로 주석처리 해제하지 말 것
        #submit_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[3]").click()

    except Exception as e:
        return False
    finally:
        return True