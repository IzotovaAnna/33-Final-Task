import pytest
from selenium import webdriver
from setting import drv_path
import uuid


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Функция помогает обнаружить, что какой-то тест не пройден.

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    test_num = str(uuid.uuid4())
    print(f"\nTest number: {test_num}\n")


    yield browser

    if request.node.rep_call.failed:
        # Сделайте скриншот, если тест не прошёл.
        try:
            browser.execute_script("document.body.bgColor = 'yellow';")

            browser.save_screenshot(f'screenshots/{test_num}.png')
            print(f"\nScreenshot with error: {test_num}.png\n")

        except:
            pass
    browser.quit()