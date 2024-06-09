from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import subprocess
from page.models import AccountDB   


def sleep(a = 1.3, b= 1.5):
    time.sleep(random.uniform(a, b))


def delete_cookies_with_cdp(driver):
    driver.execute_cdp_cmd("Network.clearBrowserCookies", {})

def is_logged_in(driver):
        try:
            sleep()
            #driver.get("https://everytime.kr/")
            # 로그인 상태에서만 존재하는 요소를 찾음
            sleep()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a"))
            )
            print("logged in is_logged_in")
            return True
        except TimeoutException:
            print("Timeout in is_logged_in")
            return False
        except NoSuchElementException:
            print("No such element in is_logged_in")
            return False

class Account:
    # def __init__(self,id, password):
    #         self.id = id
    #         self.password = password
    #         self.name = ""
    #         self.driver = self.initialize_driver()
    #         self.login()
            
    @staticmethod
    def initialize_driver():
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--log-level=3")
        #options.add_argument("--profile-default-content-settings.cookies=1")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
        subprocess.Popen(r'C:\\Program Files\\Google\\Chrome\Application\\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\chromeCookie"')
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver =  webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver
    
    
    @staticmethod
    def login(request, driver = None):
        try:
            
            if driver is None or not is_logged_in(driver) :
                driver = Account.initialize_driver()
                print("not logged in")
                
                delete_cookies_with_cdp(driver)

                
                if driver is not None:
                    print("driver is not none")
                else:
                    print("driver is none")
                driver.implicitly_wait(5)

                driver.get("https://account.everytime.kr/login")
             
                driver.implicitly_wait(5)
                id = request.session.get('id')
                password = request.session.get('password')
                print(f"id : {id}, password : {password}")

                id_box = driver.find_element(By.NAME, "id")
                id_box.send_keys(id)
                #actions.move_to_element(id_box).click_and_hold().send_keys(self.id).move_by_offset(5, 5).release().perform()
                
                pw_box = driver.find_element(By.NAME, "password")
                pw_box.send_keys(password)
                #actions.move_to_element(pw_box).click_and_hold().send_keys(self.password).move_by_offset(5, 5).release().perform()
            
                submit_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input")
                sleep()
                submit_box.click()
                #actions.move_to_element(submit_box).click_and_hold().move_by_offset(5, 5).release().perform()
                driver.implicitly_wait(5)
                print("login success")
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
            print(f"login error {e}")
            return None


    