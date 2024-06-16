import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException

class WebDriverManager:
    _instance = None

    def __init__(self):
        self.driver = None
        self.lock = threading.Lock()
        self.default_options = self._create_default_options()
        self.DRIVER_STATE = False

    @staticmethod
    def get_instance():
        if WebDriverManager._instance is None:
            WebDriverManager._instance = WebDriverManager()
        return WebDriverManager._instance

    def _create_default_options(self):
        options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def get_driver(self, custom_options=None):
        with self.lock:
   
            if self.driver is None or self.DRIVER_STATE is False:
                options = self.default_options
                if custom_options:
                    for argument in custom_options.arguments:
                        options.add_argument(argument)
                    for experimental_option, value in custom_options.experimental_options.items():
                        options.add_experimental_option(experimental_option, value)
                try:                  
                   self.driver = webdriver.Chrome(options=options)
                except SessionNotCreatedException:
                    return None
            self.DRIVER_STATE = True

            return self.driver

    def stop_driver(self):
        with self.lock:
            if self.driver is not None:
                try:
                    self.DRIVER_STATE = False
                    self.driver.close()
                    self.driver = None
                except Exception as e:
                    pass
    
    def is_stable(self):
        with self.lock:
            if self.driver is not None:
                try:
                    self.driver.current_url
                    return True
                except Exception as e:
                    self.stop_driver()
                    return False
            else:
                return False
  
            
    def switch_to_headless(self):
        with self.lock:
            if self.driver is not None:
                # 현재 쿠키와 URL을 저장
                cookies = self.driver.get_cookies()
                url = self.driver.current_url

                headless_options = self._create_default_options()
                headless_options.add_argument("--headless")

                # 기존 드라이버 종료
                self.driver.quit()
                
                # headless 모드로 옵션 설정
                options = self.default_options
                #options.add_argument("--headless")
                
                # 새로운 headless 드라이버 시작
                self.driver = webdriver.Chrome(options=headless_options)
                self.driver.get(url)
                
                # 쿠키 복원
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()


    @classmethod
    def get_instance(cls):
        if cls._instance is None or not cls._instance.is_valid_instance():
            cls._instance = WebDriverManager()
        return cls._instance