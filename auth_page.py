from base_page import BasePage
from locators import AuthLocators
from setting import site
import os
from selenium.common.exceptions import NoSuchElementException


class AuthPage(BasePage):

    def __init__(self, driver,timeout=10):
        super().__init__(driver, timeout)
        url = os.getenv("LOGIN_URL") or site
        driver.get(url)
        # Установка неявного ожидания загрузки страницы
        driver.implicitly_wait(3)

        # Табы
        self.tab_phone = driver.find_element(*AuthLocators.TAB_PHONE)
        self.tab_email = driver.find_element(*AuthLocators.TAB_EMAIL)
        self.tab_login = driver.find_element(*AuthLocators.TAB_LOGIN)
        self.tab_ls = driver.find_element(*AuthLocators.TAB_LS)

        # Подпись поля ввода username
        self.title_username = driver.find_element(*AuthLocators.TITLE_USERNAME)

        # Слоган
        self.ad_slogan = driver.find_element(*AuthLocators.AD_RT)

        # Ссылка "Забыл пароль"
        self.forgot_pass = driver.find_element(*AuthLocators.FORGOT_PASS)

        # Ссылка "Зарегистрироваться"
        self.new_reg = driver.find_element(*AuthLocators.NEW_REG)

        # Ссылка "Пользовательское соглашение"
        self.user_agree = driver.find_element(*AuthLocators.USER_AGREE)

        # Вывод ошибок
        try:
            self.err_msg = driver.find_element(*AuthLocators.ERR_MSG)
        except NoSuchElementException:
            self.err_msg = None

        # Капча
        self.captcha = True
        try:
            driver.find_element(*AuthLocators.CAPTCHA)
        except NoSuchElementException:
            self.captcha = False

        # Ввод данных
        self.username = driver.find_element(*AuthLocators.AUTH_USERNAME)
        self.password = driver.find_element(*AuthLocators.AUTH_PASS)
        self.btn = driver.find_element(*AuthLocators.AUTH_BTN)

    def swich_tab(self, tab_name):
        """ Переключение табов """
        return tab_name.click()

    def enter_username(self, value):
        """ Ввод username """
        self.username.send_keys(value)

    def enter_pass(self, value):
        """ Ввод пароля """
        self.password.send_keys(value)

    def btn_click(self):
        """ Клик по кнопке Войти """
        self.btn.click()