from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

HOMEPAGE = "http://www.scotiabank.com/jm/en/0,,27,00.html"

chrome_options = Options()


class ScotiaBankSite(object):

    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)

    def login(self, account_number=None, password=None):
        self.home_page.go_to_login_page()
        self.login_page.login(account_number=account_number, password=password)


class BasePage(object):

    def __init__(self, driver=None):
        self.driver = driver


class HomePage(BasePage):

    def go_to_login_page(self):
        """ Carries us to the login page
        """
        self.driver.get(HOMEPAGE)
        sign_in_btn = self.driver.find_element_by_id("sign-in-btn")
        print("Clicking Sign In")
        sign_in_btn.click()        


class LoginPage(BasePage):

    def login(self, account_number=None, password=None):
        self.driver.find_element_by_id(
            "contentForm:nscard").send_keys(account_number)
        self.driver.find_element_by_id(
            "contentForm:pwdnMasked").send_keys(password)
        print("Logging In")
        self.driver.find_element_by_id("contentForm:signIn").click()
        print(self.driver.current_url)

