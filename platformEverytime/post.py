from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from page.models import ContentDB, FileDB
from .account import sleep, is_logged_in

class Post:
    @staticmethod
    def post(driver, text, images=None):
        sleep()
        if not is_logged_in(driver):
            print("not logged in")
            return None
        try:
            driver.get("https://everytime.kr/")
            sleep()

            free_field_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[4]/div[1]/div/h3/a")
            free_field_box.click()
            sleep()
            post_text = driver.find_element(By.NAME, "text")
            post_text.send_keys(text)
            sleep()
            if image != 0:
                post_image = driver.find_element(By.NAME, "file")
                post_image.send_keys(image)
            sleep()
            post_submit = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[3]/form/input[3]")
            post_submit.click()
            sleep(2, 3)

            set_anonym = driver.find_element(By.CLASS_NAME, "anonym")
            set_anonym.click()
            sleep(5,7)
            for image in images:
                # 업로드 아이콘 //*[@id="container"]/div[5]/form/ul/li[2]
                print(image)
                sleep()
                image_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/ul/li[2]")
                image_box.click()
                sleep()
                upload_box = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[5]/form/input")
                upload_box.send_keys(image)
                sleep()

            return True
        except:
            print("post error")
            return False