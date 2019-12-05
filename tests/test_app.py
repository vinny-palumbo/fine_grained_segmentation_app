import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome



APP_ADDRESS = 'http://0.0.0.0:5000/'

def get_browser(headed=False) -> Chrome:
    chrome_options = Options()
    if not headed:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=chrome_options)
    return browser
    

@pytest.fixture()
def browser_headed():
    browser = get_browser(headed=False)
    yield browser
    browser.close()

    

def test_get_homepage(browser_headed: Chrome):
    browser_headed.get(APP_ADDRESS)
    assert browser_headed.current_url == APP_ADDRESS


    
    