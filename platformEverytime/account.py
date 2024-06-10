from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from page.models import AccountDB   
from .utils import sleep, delete_cookies_with_cdp, is_logged_in, quit_driver_forcefully

prefs={
    "profile.managed_default_content_settings.images": 2,  # 이미지 로드 비활성화
    "profile.managed_default_content_settings.stylesheets": 2,  # CSS 로드 비활성화
    #"profile.managed_default_content_settings.javascript": 1  # 자바스크립트 비활성화 (필요시 활성화)
}



class Account:
            
    @staticmethod
    def initialize_driver():
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument("--remote-debugging-port=9222")
        #options.add_argument("--profile-default-content-settings.cookies=1")
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        # subprocess.Popen(r'C:\\Program Files\\Google\\Chrome\Application\\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chromeCookie"')
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:8000")
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    
    
    @staticmethod
    def login(request, driver = None):
        try:
            
            if driver is None:
                driver = Account.initialize_driver()
                print("not logged in")
                
                delete_cookies_with_cdp(driver)


                driver.get("https://account.everytime.kr/login")
             
                id = request.session.get('id')
                password = request.session.get('password')
                print(f"id : {id}, password : {password}")

                WebDriverWait(driver, 10)
                id_box = driver.find_element(By.NAME, "id")
                id_box.send_keys(id)
                
                pw_box = driver.find_element(By.NAME, "password")
                pw_box.send_keys(password)
                
                submit_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
                sleep(15,16)
                submit_box.click()
                
                print("login success")
                #WebDriverWait(driver,10)
                sleep(2,3)
                name_box = driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]').text
                request.session['username'] = name_box
                request.session.save()
                print(f"nickname : {request.session['username']}")
                exist = AccountDB.objects.filter(platform = "everytime", name = name_box)
                if not exist:
                    AccountDB.objects.create(
                    platform = "everytime",
                    token = "none",
                    name = name_box,
                    tag = "none",
                    connected=True,
                    ).save()
                print("new login")
                return driver
            else:
                print("already logged in")
                return driver
        except Exception as e:
            quit_driver_forcefully(driver)
            print("login error", e)
            print("driver quitting forcefully in login")
            return None