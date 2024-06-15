from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page.models import ContentDB, FileDB
from .utils import sleep
from .account import Account
from django.db.models import Count, Max
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


# 포스트 하나하나 들어가서 이미지, icon 다 긁어오기
MAX_POSTS = 10
IMAGE_MAX = 5
ATTEMPTS = 5 # 시도 횟수

def safe_click(driver, xpath):
    attempts = 0
    while attempts < 5:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            sleep()
            return element
        except StaleElementReferenceException:
            attempts += 1
            sleep()
    raise Exception(f"Failed to click on element with xpath: {xpath} after {attempts} attempts")

def safe_get_text(driver, by, value):
    attempts = 0
    while attempts < 5:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
            return element.text
        except StaleElementReferenceException:
            attempts += 1
            sleep()
    raise Exception(f"Failed to get text from element with {by} and value: {value} after {attempts} attempts")


def safe_get_attribute(driver, by, value, attribute):
    attempts = 0
    while attempts < ATTEMPTS:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, value))
            )
            return element.get_attribute(attribute)
        except StaleElementReferenceException:
            attempts += 1
            sleep()
    raise Exception(f"Failed to get attribute from element with {by} and value: {value} after {attempts} attempts")







def Content(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a"))
        )
        sleep()
        test_xpath = '//*[@id=\"submenu\"]/div/div[12]/ul/li[1]/a'
        free_xpath = '//*[@id="submenu"]/div/div[2]/ul/li[1]/a'
        free_field_box = driver.find_element(By.XPATH, free_xpath)
        free_field_box.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"writeArticleButton\"]"))
        )
        sleep()
        
        for i in range(MAX_POSTS, 0, -1):
            post_xpath = f'//*[@id="container"]/div[5]/article[{i}]/a'
            #info = driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
            
            post = safe_click(driver, post_xpath)

            post_title = safe_get_text(driver, By.XPATH, '//*[@id="container"]/div[5]/article/a/h2')

            post_text = safe_get_text(driver, By.XPATH, '//*[@id="container"]/div[5]/article/a/p')

            post_user = safe_get_text(driver, By.XPATH, '//*[@id="container"]/div[5]/article/a/div[1]/h3')

            post_icon = safe_get_attribute(driver, By.XPATH, "//*[@id=\"container\"]/div[5]/article/a/img", "src")

            post_vote = safe_get_text(driver, By.XPATH, '//*[@id="container"]/div[5]/article/a/ul[2]/li[1]')

            image_list = []
            try:
                for i in range(1, IMAGE_MAX+1):
                    try:                                             
                        images = safe_get_attribute(driver, By.XPATH, f'//*[@id="container"]/div[5]/article/a/div[2]/figure[{i}]/img', "src")
                       
                        image_list.append(images)
                    except:
                        break
            except:
                images = safe_get_attribute(driver, By.XPATH, "//*[@id=\"container\"]/div[5]/article/a/div[2]/figure/img", "src")
                if images:
                    image_list.append(images)

 
            latest = FileDB.objects.aggregate(max_uid=Max('uid'))['max_uid']
            if latest is None:
                latest = 0  # 최신 값이 없으면 0으로 초기화

            image_url = 0
            
            if image_list:
                last = 0
                for i, image in enumerate(reversed(image_list), start=last):
                    image_url = latest + 1
                    
                    FileDB.objects.create(
                        uid=image_url,
                        url=image,
                    ).save()

            
            ContentDB.objects.create(
                platform = "Everytime",
                userID = post_user,
                text = post_title+"|||" + post_text,
                image_url = image_url,
                userIcon = post_icon,
                vote = post_vote,
            ).save()   
            driver.back()    
            sleep()
            
    except Exception as e:
        return False
    return True
