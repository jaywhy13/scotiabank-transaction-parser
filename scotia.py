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
        result = self.login_page.answer_security_question(answer)
        self.current_page = ScotiaBankSite.PAGE_ACCOUNTS
        return result

    def get_accounts(self):
        return self.accounts_page.get_accounts()


class BasePage(object):

    def __init__(self, driver=None):
        self.driver = driver


class LoginPage(BasePage):
    """ An ecanpsulation of the login page, allows us to do just that.. login
    """

    LOGIN_ERROR_SELECTOR = "span.alert-msg"
    SECURITY_QUESTION_INPUT = "#contentForm .RUIFW-form-el"
    ANSWER_SECURITY_QUESTION_BUTTON = "#contentForm .RUIFW-btn-primary"

    def login(self, account_number=None, password=None):
        """ Logs in to the website using an account number and password
        """
        self.driver.get(LOGIN_PAGE)
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


class AccountsPage(BasePage):

    ACCOUNT_NUMBER_REGEX = \
        r'(?P<account_name>.*) \- (?P<branch_code>[0-9]+) ?(?P<account_number>[0-9]+)'

    def get_accounts(self):
        """ Returns a list of the accounts on the page
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "td.account-type")))
        accounts = []
        elements = self._get_account_elements()
        for element in elements:
            balance = self._get_account_balance(element)
            name = self._get_account_name(element)
            account_number = self._get_account_number(element)
            branch_code = self._get_branch_code(element)
            accounts.append({
                "name": name,
                "balance": balance,
                "account_number": account_number,
                "branch_code": branch_code,
            })
        return accounts

    def _get_account_elements(self):
        """ Returns the list of elements containing our accounts
        """
        return self.driver.find_elements_by_css_selector("td.account-type")

    def _get_account_name(self, element):
        text = element.text.strip().replace("\n", "")
        match = \
            re.match(AccountsPage.ACCOUNT_NUMBER_REGEX, text)
        name = match.group('account_name')
        return name

    def _get_account_balance(self, element):
        parent = element.find_element_by_xpath('..')
        balance = parent.find_element_by_css_selector(
            ".balance").text
        return balance

    def _get_branch_code(self, element):
        text = element.text.strip().replace("\n", "")
        match = \
            re.match(AccountsPage.ACCOUNT_NUMBER_REGEX, text)
        branch_code = match.group('branch_code')
        return branch_code

    def _get_account_number(self, element):
        text = element.text.strip().replace("\n", "")
        match = \
            re.match(AccountsPage.ACCOUNT_NUMBER_REGEX, text)
        account_number = match.group('account_number')
        return account_number


    def go_to_account(self, branch_code=None, account_number=None):
        """ Goes to the account details page for the given account
        """
        print("Going to account page for: {} {}".format(
            branch_code, account_number))
        for element in self._get_account_elements():
            if self._get_branch_code(element) == branch_code and \
                    self._get_account_number(element) == account_number:
                a = element.find_element_by_tag_name("a")
                print("Clicking on {}".format(a.text))
                a.click()
                self.current_page = ScotiaBankSite.PAGE_ACCOUNT
                return
        raise Exception(
            "Could not find account page for {} {}".format(
                branch_code, account_number))


class AccountPage(BasePage):

    DATE_LIST_SELECTOR_ID = "transDetailsForm:date_list"
    TRANSACTIONS_TABLE_ID = "transDetailsForm:current"

    def get_transactions(self, branch_code=None, account_number=None):
        """ Returns the list of transactions on the page
        """
        self.select_this_month_transactions()
        transactions = self._get_transasctions_from_table()
        return transactions

    def select_this_month_transactions(self):
        """ This selects this months' transactions from the drop down on
            the account details page
        """
        element = self.driver.find_element_by_id(
            AccountPage.DATE_LIST_SELECTOR_ID)
        options = element.find_elements_by_tag_name("option")
        for option in options:
            if option.text.strip() == "This Month":
                option.click()

    def _get_transasctions_from_table(self):
        transactions = []
        table = self.driver.find_element_by_id(
            AccountPage.TRANSACTIONS_TABLE_ID)
        trs = table.find_elements_by_tag_name("tr")
        for tr in trs:
            tds = tr.find_elements_by_tag_name("td")
            print("Found {} tds in {}".format(len(tds), tr.text))
            if len(tds) >= 3:
                date = tds[0].text.strip()
                description = tds[1].text.strip()
                amount = tds[3].text.strip()
                transactions.append({
                    "date": date,
                    "description": description,
                    "amount": amount
                })
        return transactions
