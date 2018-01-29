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
        """ Logs in to the website. Raises an exception if login fails

            :param str account_number - the account number
            :param str password - the password for the account
        """
        self.home_page.go_to_login_page()
        return self.login_page.login(
            account_number=account_number, password=password)


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
    """ An ecanpsulation of the login page, allows us to do just that.. login
    """

    LOGIN_ERROR_SELECTOR = "span.alert-msg"

    def login(self, account_number=None, password=None):
        """ Logs in to the website using an account number and password
        """
        self.try_to_login(
            account_number=account_number, password=password)
        if self.is_logged_in():
            print("Logged in successfully")
            return True
        login_error = self.get_login_error()
        self.driver.close()
        raise Exception(login_error)

    def try_to_login(self, account_number=None, password=None):
        """ Attempt login
        """
        self.driver.find_element_by_id(
            "contentForm:nscard").send_keys(account_number)
        self.driver.find_element_by_id(
            "contentForm:pwdnMasked").send_keys(password)
        print("Logging In")
        self.driver.find_element_by_id("contentForm:signIn").click()

    def is_logged_in(self):
        """ Tells us if login was successful
        """
        return "Security question" in self.driver.page_source

    def get_login_error(self):
        """ Returns the login error on the page
        """
        span = self.driver.find_element_by_css_selector(
            LoginPage.LOGIN_ERROR_SELECTOR)
        return span.text

    def get_security_question(self):
        question = self.driver.find_element_by_css_selector(
            ".RUIFW-col-12 span").text
        return question
