import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import SessionNotCreatedException
class WebDriverManager:
    _instance = None

    def __init__(self):
        self.driver = None
        self.lock = threading.Lock()
        self.default_options = self._create_default_options()

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
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def get_driver(self, custom_options=None):
        with self.lock:
            if self.driver is None:
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
            return self.driver

    def stop_driver(self):
        with self.lock:
            if self.driver is not None:
                self.driver.close()
                self.driver = None
    
    def is_stable(self):
        with self.lock:
            if self.driver is not None:
                try:
                    self.driver.current_url
                    return True
                except Exception as e:
                    return False
            else:
                return False