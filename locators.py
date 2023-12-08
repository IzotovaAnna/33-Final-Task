from selenium.webdriver.common.by import By

class AuthLocators:
    # Поля ввода
    AUTH_USERNAME = (By.ID, "username")
    AUTH_PASS = (By.ID, "password")

    # Кнопка
    AUTH_BTN = (By.ID, "kc-login")

    # Табы
    TAB_PHONE = (By.ID, "t-btn-tab-phone")
    TAB_EMAIL = (By.ID, "t-btn-tab-mail")
    TAB_LOGIN = (By.ID, "t-btn-tab-login")
    TAB_LS = (By.ID, "t-btn-tab-ls")

    # Подпись в поле ввода username
    TITLE_USERNAME = (By.CSS_SELECTOR, "div.tabs-input-container__login span.rt-input__placeholder")

    # Слоган
    AD_RT = (By.CSS_SELECTOR, "p.what-is__desc")

    # Ссылка "Забыл пароль"
    FORGOT_PASS = (By.ID, "forgot_password")

    # Ссылка "Зарегистрироваться"
    NEW_REG = (By.ID, "kc-register")

    # Ссылка "Пользовательское соглашение"
    USER_AGREE = (By.CSS_SELECTOR, "div.auth-policy a")

    # Ошибки
    ERR_MSG = (By.ID, "form-error-message")

    # Капча
    CAPTCHA = (By.ID, "captcha")