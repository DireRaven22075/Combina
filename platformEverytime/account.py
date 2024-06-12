from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page.models import AccountDB   
from .utils import sleep, delete_cookies_with_cdp, is_logged_in, quit_driver_forcefully
import logging
prefs={
    "profile.managed_default_content_settings.images": 2,  # 이미지 로드 비활성화
    "profile.managed_default_content_settings.stylesheets": 2,  # CSS 로드 비활성화
    #"profile.managed_default_content_settings.javascript": 1  # 자바스크립트 비활성화 (필요시 활성화)
}



class Account:
    def __init__(self, request):
        self.request = request
        self.id = request.session.get('ev_id')
        self.password = request.session.get('ev_password')
        self.username = request.session.get('username', 'none')
        self.driver = Account.initialize_driver()
        self.driver = self.login()


    @staticmethod
    def initialize_driver():
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless") # 브라우저 띄우지 않음
        options.add_argument("--log-level=3")
        options.add_argument("--remote-debugging-port=9222")
        #options.add_argument("--profile-default-content-settings.cookies=1") # 쿠키 허용
        # subprocess.Popen(r'C:\\Program Files\\Google\\Chrome\Application\\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chromeCookie"')
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:8000") # 디버거 주소
        #options.add_experimental_option("prefs", prefs) # 이미지, CSS, 자바스크립트 로드 설정
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    
    
    def login(self):
        try:
                      
            delete_cookies_with_cdp(self.driver)


            self.driver.get("https://account.everytime.kr/login")
            
            

            WebDriverWait(self.driver, 10).until(EC.new_window_is_opened)
            sleep()
            id_box = self.driver.find_element(By.NAME, "id")
            id_box.send_keys(self.id)
            
            pw_box = self.driver.find_element(By.NAME, "password")
            pw_box.send_keys(self.password)
            
            submit_box = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
            sleep(15,16)
            submit_box.click()
     
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]'))
            )
            sleep()
            name_box = self.driver.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[1]/form/p[1]').text
            id_name = self.driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[1]/div[1]/form/p[3]").text
            icon_image = self.driver.find_element(By.XPATH, "//*[@id=\"container\"]/div[1]/div[1]/form/img").get_attribute("src")
            
            
            self.request.session['username'] = name_box
            self.request.session.save()

            exist = AccountDB.objects.filter(platform = "Everytime", name = name_box)
            if not exist:
                AccountDB.objects.create(
                platform = "Everytime",
                token = "none",
                name = name_box,
                tag = id_name,
                connected=True,
                icon = icon_image
                ).save()
            else:
                AccountDB.objects.filter(platform = "Everytime", name = name_box).update(connected=True)
                AccountDB.objects.filter(platform = "Everytime", name = name_box).update(icon = icon_image)
                AccountDB.objects.filter(platform = "Everytime", name = name_box).update(tag = id_name)
            return self.driver

           
        except Exception as e:
            quit_driver_forcefully(self.driver)
            return None
    
    def __del__(self):
        try:
            if self.driver is not None:
                self.driver.close()
        except Exception as e:
            logging.error("driver close error: %s", e)