import os
import pytest
import selenium
import numpy as np
import imageio
from tempfile import mkdtemp
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome



APP_ADDRESS = 'http://localhost:5000/'


def make_folder_with_an_image(resolution = (300, 300), channels = 3):
    # create temp folder
    temp_dir = mkdtemp()

    # create random image
    img = np.random.randint(0, high=256, size=(*resolution, channels), dtype=np.uint8)
    file_path = os.path.join(temp_dir, "some-image.jpg")
    imageio.imsave(file_path, img)

    return temp_dir


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


def test_app_address_doesnt_change_when_clicking_on_upload_button(browser_headed: Chrome):
    browser_headed.get(APP_ADDRESS)
    upload_button = browser_headed.find_element_by_class_name("choose-file-button")
    upload_button.click()
    assert browser_headed.current_url == APP_ADDRESS


def test_alert_triggered_when_clicking_on_apply_segmentation_with_no_input(browser_headed: Chrome):
    browser_headed.get(APP_ADDRESS)
    
    # apply  segmentation with no input
    apply_button = browser_headed.find_element_by_id("analyze-button")
    apply_button.click()
    
    # test alert message
    alert_obj = browser_headed.switch_to.alert
    assert alert_obj.text == "Please select a file to segment!"
    
    # close alert after test completed
    alert_obj.accept() 
    
    
def test_segmentation_on_an_image(browser_headed: Chrome):
    # get the front page of app
    browser_headed.get(APP_ADDRESS)

    # create a temporary image
    folder = make_folder_with_an_image()
    filename = os.listdir(folder)[0]
    file_path = os.path.join(folder, filename)

    # input the temporary image
    file_input = browser_headed.find_element_by_id("file-input")
    file_input.send_keys(file_path);

    # apply segmentation on temporary image
    apply_button = browser_headed.find_element_by_id("analyze-button")
    apply_button.click()
    
    # test apply button text changes
    assert apply_button.text == "Segmenting Items..."

    # wait for segmentation to complete
    time.sleep(120)

    # see if result.png was generated
    result_element = browser_headed.find_element_by_id("image-picked")
    result_src = result_element.get_attribute("src")
    assert "/static/result.png" in result_src
    
    
    