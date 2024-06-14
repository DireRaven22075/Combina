import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import signal
import psutil



def sleep(a = 1.3, b= 1.5):
    time.sleep(random.uniform(a, b))


def delete_cookies_with_cdp(driver):
    driver.delete_all_cookies()
    driver.execute_cdp_cmd("Network.clearBrowserCookies", {})

def is_logged_in(driver):
        try:
            sleep()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a"))
            )
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False
        
