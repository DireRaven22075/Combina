from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from .webdriver_manager import WebDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page.models import AccountDB   
from .utils import sleep
import logging


def Account(request, driver):
    try:


        driver.get("https://account.everytime.kr/login")

        WebDriverWait(driver, 1200).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]'))
        )
        sleep(2,3)
        name_box = driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]').text
        id_name = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[1]/div[1]/form/p[3]").text
        icon_image = driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[1]/div[1]/form/img").get_attribute("src")
        
        request.session['username'] = name_box
        request.session.save()

        
        
        # 로그인 상태 AccountDb에 저장
        try:
            
            exist = AccountDB.objects.filter(platform="Everytime").last()
            if exist:
                exist.connected =True
                exist.platform="Everytime"
                exist.token = "None"
                exist.name = name_box
                exist.tag = id_name
                exist.icon = icon_image
                exist.save()        
                
            else:
                return False
        except Exception as e:
            return False
     
    except Exception as e:
        driver.close()
        return False
    return True
    
