import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auth_page import AuthPage
from setting import *


def test_tab_phone(web_browser):
    """ Проверка наличия таба Телефон на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Телефон
    page.swich_tab(page.tab_phone)
    print(page.title_username.text)
    assert page.title_username.text == u"Мобильный телефон", "FT-001 failed: Таб Телефон не найден"


def test_tab_email(web_browser):
    """ Проверка наличия таба Почта на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Почта
    page.swich_tab(page.tab_email)
    print(page.title_username.text)
    assert page.title_username.text == u"Электронная почта", "FT-002 failed: Таб Почта не найден"


def test_tab_login(web_browser):
    """ Проверка наличия таба Логин на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Логин
    page.swich_tab(page.tab_login)
    print(page.title_username.text)
    assert page.title_username.text == u"Логин", "FT-003 failed: Таб Логин не найден"


def test_tab_ls(web_browser):
    """ Проверка наличия таба Лицевой счет на странице авторизации """

    page = AuthPage(web_browser)

    # Переходим на таб Лицевой счет
    page.swich_tab(page.tab_ls)
    print(page.title_username.text)
    assert page.title_username.text == u"Лицевой счёт", "FT-004 failed: Таб Лицевой счет не найден"


def test_input_field(web_browser):
    """ Проверка наличия полей ввода username и пароля на странице авторизации """

    page = AuthPage(web_browser)

    # Есть поле ввода логина
    assert page.username, "FT-005 failed: Нет поля ввода username"
    # Есть поле ввода пароля
    assert page.password, "FT-005 failed: Нет поля ввода пароля"
    # Есть кнопка "Войти"
    assert page.btn, "FT-005 failed: Нет кнопки 'Войти'"


def test_ad_slogan(web_browser):
    """ Проверка наличия слогана на странице авторизации """

    page = AuthPage(web_browser)

    assert ad_slogan in page.ad_slogan.text, f"FT-006 failed: Нет слогана {ad_slogan}"


@pytest.mark.parametrize(("username, tab_title"),
                            [
                                (valid_email, u"Почта"),
                                (valid_login, u"Логин"),
                                (valid_ls, u"Лицевой счёт"),
                                (valid_phone, u"Телефон")
                            ],
                            ids= [
                                'By email',
                                'By login',
                                "By LS",
                                "By phone"]
                         )
def test_auto_switch_tab(username, tab_title, web_browser):
    """ Автоматическая смена таба при вводе соотвествующего способа авторизации """

    page = AuthPage(web_browser)

    # Если проверяем ввод телефона, переходим предварительно на таб Почта, т.к. таб Телефон открыт по умолчанию
    if tab_title == "Телефон":
        page.swich_tab(page.tab_email)

    # Вводим логин
    page.enter_username(username)
    # Кликаем на пароль
    page.password.click()

    time.sleep(3)

    # Смотрим активный таб
    active_tab = web_browser.find_element(By.CSS_SELECTOR, "div.rt-tab--active").text
    # print(f"\n{active_tab} == {tab_title}")

    assert active_tab == tab_title, "FT-007 failed: Таб автоматически не изменился"


def test_forgot_password(web_browser):
    """ Проверка наличия ссылки "Забыл пароль" на странице авторизации """

    page = AuthPage(web_browser)

    # Кликаем по ссылке "Забыл пароль"
    page.forgot_pass.click()

    # Явное ожидание загрузки элемента div.reset-form-container - внешний контейнер формы восстановления пароля
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.reset-form-container'))
    )

    assert "Восстановление пароля" in web_browser.find_element(By.CSS_SELECTOR, 'div.reset-form-container').text, "FT-008 failed: На странице нет элемента 'Восстановление пароля'"


def test_new_reg(web_browser):
    """ Проверка наличия ссылки "Зарегистрироваться" на странице авторизации """

    page = AuthPage(web_browser)

    # Кликаем по ссылке "Зарегистрироваться"
    page.new_reg.click()

    # Явное ожидание загрузки элемента div.register-form-container - внешний контейнер формы регистрации
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.register-form-container'))
    )

    assert "Регистрация" in web_browser.find_element(By.CSS_SELECTOR, 'div.register-form-container').text, "FT-009 failed: На странице нет элемента 'Регистрация'"


def test_user_agree(web_browser):
    """ Проверка наличия ссылки "пользовательское соглашение" на странице авторизации """

    page = AuthPage(web_browser)

    # Кликаем по ссылке "пользовательское соглашение"
    page.user_agree.click()

    # Ссылка открывается в новой вкладке
    new_window = web_browser.window_handles[1]
    web_browser.switch_to.window(new_window)

    assert web_browser.current_url == 'https://b2c.passport.rt.ru/sso-static/agreement/agreement.html', "FT-010 failed: Пользовательское соглашение не загружено"


# Негативные тесты
@pytest.mark.parametrize("phone", ['', ' '], ids= ["Empty phone", "Space phone"])
def test_auth_by_empty_phone(phone, web_browser):
    """ Авторизации с пустым номером телефона """

    page = AuthPage(web_browser)

    # Переходим на таб Мобильный телефон
    page.swich_tab(page.tab_phone)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(phone)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    assert link_lk not in web_browser.current_url, f"AT-006 failed: Выполнен вход в ЛК"
    # Появляется надпись "Введите номер телефона"
    assert web_browser.find_element(By.CSS_SELECTOR, "span.rt-input-container__meta.rt-input-container__meta--error").text == 'Введите номер телефона', "AT-006 failed: нет предупреждения о пустом номере телефона"


@pytest.mark.parametrize("email", ['', ' '], ids=["Empty email", "Space email"])
def test_auth_by_empty_email(email, web_browser):
    """ Авторизации с пустым адресом электронной почты """

    page = AuthPage(web_browser)

    # Переходим на таб Почта
    page.swich_tab(page.tab_email)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(email)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Введите адрес, указанный при регистрации"
    assert web_browser.find_element(By.CSS_SELECTOR,
                                    "span.rt-input-container__meta.rt-input-container__meta--error").text == 'Введите адрес, указанный при регистрации', f"AT-011 failed: нет предупреждения о пустом емейле"


@pytest.mark.parametrize("login", ['', ' '], ids= ["Empty login", "Space login"])
def test_auth_by_empty_login(login, web_browser):
    """ Авторизации с пустым логином """

    page = AuthPage(web_browser)

    # Переходим на таб Логин
    page.swich_tab(page.tab_login)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(login)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Введите логин, указанный при регистрации"
    assert web_browser.find_element(By.CSS_SELECTOR, "span.rt-input-container__meta.rt-input-container__meta--error").text == 'Введите логин, указанный при регистрации', f"AT-016 failed: нет предупреждения о пустом логине"


@pytest.mark.parametrize("ls", ['', ' '], ids= ["Empty ls", "Space ls"])
def test_auth_by_empty_ls(ls, web_browser):
    """ Авторизации с пустым ЛС """

    page = AuthPage(web_browser)

    # Переходим на таб Логин
    page.swich_tab(page.tab_ls)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(ls)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Введите номер вашего лицевого счета"
    assert web_browser.find_element(By.CSS_SELECTOR, "span.rt-input-container__meta.rt-input-container__meta--error").text == 'Введите номер вашего лицевого счета', f"AT-018 failed: нет предупреждения о пустом ЛС"


@pytest.mark.parametrize("username, passwd, test_num", [
                            (valid_phone, '', 'AT-007'),
                            (valid_phone, ' ', 'AT-007'),
                            (valid_email, '', 'AT-012'),
                            (valid_email, ' ', 'AT-012'),
                            (valid_login, '', 'AT-017'),
                            (valid_login, ' ', 'AT-017'),
                            (valid_ls, '', 'AT-019'),
                            (valid_ls, ' ', 'AT-019')
                        ], ids= [
                            "Phone: Empty password",
                            "Phone: Space password",
                            "Email: Empty password",
                            "Email: Space password",
                            "Login: Empty password",
                            "Login: Space password",
                            "LS: Empty password",
                            "LS: Space password"
                        ])
@pytest.mark.xfail(reason="Нереализовано")
def test_auth_by_username_and_empty_password(username, passwd, test_num, web_browser):
    """ Авторизации с пустым паролем """

    page = AuthPage(web_browser)

    # Вводим логин/пароль
    page.enter_username(username)
    page.enter_pass(passwd)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Введите пароль"
    assert web_browser.find_element(By.CSS_SELECTOR, "span.rt-input-container__meta.rt-input-container__meta--error").text == 'Введите пароль', f"{test_num} failed: Нет вывода сообщения 'Введите пароль'"


@pytest.mark.parametrize("username, test_num", [
                                ('+7(999)9999999', "AT-008"),
                                ("romashka2003@gmail.com", "AT-014")
                            ], ids= [
                                "Wrong phone number",
                                "Wrong email"
                            ]
                         )
def test_auth_by_wrong_phone(username, test_num, web_browser):
    """ Авторизации неверным username и верным паролем"""

    page = AuthPage(web_browser)

    # Вводим логин/пароль
    page.enter_username(username)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        print("Captcha!!!")
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Неверный логин или пароль"
    assert web_browser.find_element(By.ID, "form-error-message").text == 'Неверный логин или пароль', f"{test_num} failed: Нет надписи 'Неверный логин или пароль'"


@pytest.mark.parametrize("username, passwd, test_num", [
                            (valid_phone, 'hjvfirf2003', 'AT-009'),
                            (valid_email, 'hjvfirf2003', 'AT-013'),
                        ], ids= [
                            "Phone: Wrong password",
                            "Email: Wrong password",
                        ])
def test_auth_by_wrong_password(username, passwd, test_num, web_browser):
    """ Авторизации верным username и неверным паролем"""

    page = AuthPage(web_browser)

    # Вводим логин/пароль
    page.enter_username(username)
    page.enter_pass(passwd)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        print("Captcha!!!")
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Неверный логин или пароль"
    assert web_browser.find_element(By.ID, "form-error-message").text == 'Неверный логин или пароль', f"{test_num} failed: Нет надписи 'Неверный логин или пароль'"


@pytest.mark.parametrize("phone", ['+7(977)561260'], ids= ["Not correct numb"])
def test_auth_by_bad_format_phone(phone, web_browser):
    """ Авторизации по номеру телефона в неверном формате"""

    page = AuthPage(web_browser)

    # Переходим на таб Мобильный телефон
    page.swich_tab(page.tab_phone)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(phone)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Появляется надпись "Введите номер телефона"
    assert web_browser.find_element(By.CSS_SELECTOR, "span.rt-input-container__meta.rt-input-container__meta--error").text == 'Неверный формат телефона', f"AT-010 failed: Нет надписи 'Неверный логин или пароль'"


@pytest.mark.parametrize("email", ['romashkacool2003@gmail'], ids= ["Not correct email"])
def test_auth_by_bad_format_email(email, web_browser):
    """ Авторизации по емейлу в неверном формате"""

    page = AuthPage(web_browser)

    # Переходим на таб Почта
    page.swich_tab(page.tab_email)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(email)
    page.enter_pass(valid_password)

    # Проверка перехода на таб "Логин"
    assert web_browser.find_element(By.CSS_SELECTOR, "div.rt-tab.rt-tab--small.rt-tab--active").text == 'Логин', f"AT-015 failed: не перешли на таб 'Логин'"

# Позитивные тесты
def test_auth_by_phone(web_browser):
    """ Авторизация по номеру телефона """

    page = AuthPage(web_browser)

    # Переходим на таб Мобильный телефон
    page.swich_tab(page.tab_phone)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(valid_phone)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)


    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Явное ожидание загрузки элемента div.home-container - внешний контейнер в ЛК
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.home-container'))
    )

    print(web_browser.current_url)
    print(f'h2.user-name[title="{valid_username}"]')
    # Проверка
    assert link_lk in web_browser.current_url, f"AT-001 failed: Текущая ссылка {web_browser.current_url} не содержит account_b2"
    assert web_browser.find_element(By.CSS_SELECTOR, f'h2.user-name[title="{valid_username}"]'), f"AT-001 failed: На странице нет элемента {valid_username}"


def test_auth_by_email(web_browser):
    """ Авторизация по емейлу """

    page = AuthPage(web_browser)

    # Переходим на таб Почта
    page.swich_tab(page.tab_email)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(valid_email)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Явное ожидание загрузки элемента div.home-container - внешний контейнер в ЛК
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.home-container'))
    )

    print(web_browser.current_url)
    print(f'h2.user-name[title="{valid_username}"]')
    # Проверка
    assert link_lk in web_browser.current_url, f"AT-002 failed: Текущая ссылка {web_browser.current_url} не содержит account_b2"
    assert web_browser.find_element(By.CSS_SELECTOR, f'h2.user-name[title="{valid_username}"]'), f"AT-002 failed: На странице нет элемента {valid_username}"


@pytest.mark.skip("При регистрации не был получен логин, позитивный тест невозможен")
def test_auth_by_login(web_browser):
    """ Авторизация по логину """

    page = AuthPage(web_browser)

    # Переходим на таб Логин
    page.swich_tab(page.tab_login)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(valid_login)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Явное ожидание загрузки элемента div.home-container - внешний контейнер в ЛК
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.home-container'))
    )

    print(web_browser.current_url)
    print(f'h2.user-name[title="{valid_username}"]')
    # Проверка
    assert link_lk in web_browser.current_url, f"AT-003 failed: Текущая ссылка {web_browser.current_url} не содержит account_b2"
    assert web_browser.find_element(By.CSS_SELECTOR, f'h2.user-name[title="{valid_username}"]'), f"AT-003 failed: На странице нет элемента {valid_username}"


@pytest.mark.skip("Без подключения услуги нет лицевого счета, позитивный тест невозможен")
def test_auth_by_ls(web_browser):
    """ Авторизация по лицевому счету """

    page = AuthPage(web_browser)

    # Переходим на таб Лицевой счет
    page.swich_tab(page.tab_ls)
    print(page.title_username.text)

    # Вводим логин/пароль
    page.enter_username(valid_ls)
    page.enter_pass(valid_password)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Явное ожидание загрузки элемента div.home-container - внешний контейнер в ЛК
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.home-container'))
    )

    print(web_browser.current_url)
    print(f'h2.user-name[title="{valid_username}"]')
    # Проверка
    assert link_lk in web_browser.current_url, f"AT-004 failed: Текущая ссылка {web_browser.current_url} не содержит account_b2"
    assert web_browser.find_element(By.CSS_SELECTOR, f'h2.user-name[title="{valid_username}"]'), f"AT-004 failed: На странице нет элемента {valid_username}"


@pytest.mark.parametrize(("username, username_title"),
                            [
                                (valid_email, u"Почта"),
                                #(valid_login, u"Логин"),
                                #(valid_ls, u"Лицевой счёт"),
                                (valid_phone, u"Телефон")
                            ],
                            ids= [
                                'By email',
                                #'By login',
                                #"By LS",
                                "By phone"]
                         )
def test_auth_in_any_tab(username, username_title, web_browser):
    """ Авторизация по любому username без смены таба """

    page = AuthPage(web_browser)

    # Если проверяем ввод телефона, переходим предварительно на таб Почта, т.к. таб Телефон открыт по умолчанию
    if username_title == "Телефон":
        page.swich_tab(page.tab_email)

    # Вводим логин/пароль
    page.enter_username(username)
    page.enter_pass(valid_password)

    print(username_title)

    # Если есть капча, делаем задержку для ввода капчи
    if page.captcha:
        time.sleep(20)

    # Нажимаем кнопку "Войти"
    page.btn_click()

    # Явное ожидание загрузки элемента div.home-container - внешний контейнер в ЛК
    WebDriverWait(web_browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.home-container'))
    )

    print(web_browser.current_url)
    print(f'h2.user-name[title="{valid_username}"]')
    # Проверка
    assert link_lk in web_browser.current_url, f"AT-005 failed: Текущая ссылка {web_browser.current_url} не содержит account_b2"
    assert web_browser.find_element(By.CSS_SELECTOR, f'h2.user-name[title="{valid_username}"]'), f"AT-005 failed: На странице нет элемента {valid_username}"
