# tests/test_e2e.py
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

APP_URL = "http://127.0.0.1:5000"



@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # headless pour CI; retire si tu veux voir le navigateur
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


def test_e2e_register_login_create_task(driver):
    # ATTENTION: l'app doit être démarrée localement : python app.py
    driver.get(APP_URL + "/register")
    time.sleep(0.5)

    # remplir le formulaire de register
    driver.find_element(By.NAME, "username").send_keys("e2euser")
    driver.find_element(By.NAME, "password").send_keys("e2epass")
    driver.find_element(By.NAME, "confirm").send_keys("e2epass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(0.5)

    # after register, should redirect to login
    driver.get(APP_URL + "/login")
    time.sleep(0.5)

    # login
    driver.find_element(By.NAME, "username").send_keys("e2euser")
    driver.find_element(By.NAME, "password").send_keys("e2epass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(0.5)

    # go to create task page
    driver.get(APP_URL + "/tasks/new")
    time.sleep(0.5)
    driver.find_element(By.NAME, "title").send_keys("E2E Task")
    driver.find_element(By.NAME, "description").send_keys("Created by e2e test")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(0.5)

    # back to index and assert task text is present in page source
    driver.get(APP_URL + "/")
    time.sleep(0.5)
    assert "E2E Task" in driver.page_source
