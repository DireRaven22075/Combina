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
        

def quit_driver_forcefully(driver):
    try:
        driver.quit()
    except:
        # 드라이버 프로세스 강제 종료
        driver_process = driver.service.process
        if driver_process:
            try:
                # 드라이버 프로세스의 PID를 가져옴
                driver_pid = driver_process.pid
                
                # 프로세스 종료
                driver_process.terminate()
                driver_process.wait(timeout=3)  # 종료 완료까지 대기
                
                # 프로세스가 종료되었는지 확인
                if not psutil.pid_exists(driver_pid) or psutil.Process(driver_pid).status() == psutil.STATUS_ZOMBIE:
                    print("Driver process terminated successfully.")
                else:
                    # 남아있는 프로세스가 있다면 강제로 종료
                    os.kill(driver_pid, signal.SIGKILL)
                    print("Driver process terminated forcefully.")
            except Exception as e:
                print("Error occurred while terminating driver process:", e)