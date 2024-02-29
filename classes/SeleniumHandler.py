from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import parse_qs, urlparse


class SeleniumHandler:
    def __init__(self):
        self.driver = None

    def start_driver(self, chrome_options=None):
        if chrome_options is None:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--log-level=3")

        chrome_service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def get_url(self, url):
        if not self.driver:
            raise ValueError("Driver não inicializado. Chame 'start_driver()' primeiro.")

        self.driver.get(url)

    def find_element(self, by, value):
        if not self.driver:
            raise ValueError("Driver não inicializado. Chame 'start_driver()' primeiro.")

        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            raise NoSuchElementException(f"Elemento não encontrado com {by}={value}")

    def find_elements(self, by, value):
        if not self.driver:
            raise ValueError("Driver não inicializado. Chame 'start_driver()' primeiro.")

        try:
            elements = self.driver.find_elements(by, value)
            return elements
        except NoSuchElementException:
            raise NoSuchElementException(f"Elementos não encontrados com {by}={value}")

    def wait_for_element(self, by, value, timeout=5):
        if not self.driver:
            raise ValueError("Driver não inicializado. Chame 'start_driver()' primeiro.")

        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            raise TimeoutException(f"Elemento {value} não encontrado após {timeout} segundos.")

    def execute_script(self, script, element=None):
        if not self.driver:
            raise ValueError("Driver não inicializado. Chame 'start_driver()' primeiro.")

        if element:
            self.driver.execute_script(script, element)
        else:
            self.driver.execute_script(script)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
