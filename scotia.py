from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

HOMEPAGE = "http://www.scotiabank.com/jm/en/0,,27,00.html"
LOGIN_PAGE = \
    "https://www1.online.scotiabank.com/onlineV1/leap/signon/signOn.xhtml?" \
    "country=JAM&lang=en&channel=WEB"

chrome_options = Options()


class ScotiaBankSite(object):

    PAGE_LOGIN = 'login'
    PAGE_SECURITY_QUESTION = 'security-question'
    PAGE_ACCOUNTS = 'accounts'
    PAGE_ACCOUNT = 'account'

    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.login_page = LoginPage(self.driver)
        self.accounts_page = AccountsPage(self.driver)
        self.current_page = ScotiaBankSite.PAGE_LOGIN


    def login(self, account_number=None, password=None):
        """ Logs in to the website. Raises an exception if login fails

            :param str account_number - the account number
            :param str password - the password for the account
        """
        result = self.login_page.login(
            account_number=account_number, password=password)
        self.current_page = ScotiaBankSite.PAGE_SECURITY_QUESTION
        return result

    def get_security_question(self):
        """ Returns the security question on the page
        """
        return self.login_page.get_security_question()

    def answer_security_question(self, answer):
        return self.login_page.answer_security_question(answer)
        self.current_page = ScotiaBankSite.PAGE_ACCOUNTS


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
    SECURITY_QUESTION_INPUT = "#contentForm .RUIFW-form-el"
    ANSWER_SECURITY_QUESTION_BUTTON = "#contentForm .RUIFW-btn-primary"

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

    def answer_security_question(self, answer):
        print("Entering answer")
        self.driver.find_element_by_css_selector(
            LoginPage.SECURITY_QUESTION_INPUT).send_keys(answer)
        print("Submitting answer")
        self.driver.find_element_by_css_selector(
            LoginPage.ANSWER_SECURITY_QUESTION_BUTTON).click()
        print("Checking for errors")
        error_message = self.get_security_question_error()
        if error_message:
            raise Exception(error_message)
        return True

    def get_security_question_error(self):
        try:
            error_icon = self.driver.find_element_by_css_selector(
                ".alert-icon-error")
            message = \
                self.driver.find_element_by_css_selector(
                    LoginPage.LOGIN_ERROR_SELECTOR).text
            return message
        except NoSuchElementException as e:
            return ''
