from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

UI_URL = "http://127.0.0.1:5500"

def test_ui_register_and_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(UI_URL)
        time.sleep(2)

        # UNIQUE EMAIL
        email = f"user{int(time.time())}@test.com"
        password = "Password@123"

        # Register
        driver.find_element(By.XPATH, "//input[@placeholder='email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='password (min 6)']").send_keys(password)
        driver.find_element(By.XPATH, "//button[text()='Register']").click()
        time.sleep(2)

        # Login
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(2)

        # Assert login success
        assert "Not logged in" not in driver.page_source

    finally:
        time.sleep(2)
        driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
import time

UI_URL = "http://127.0.0.1:5500"

def test_ui_register_and_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(UI_URL)
        time.sleep(2)

        email = f"user{int(time.time())}@test.com"
        password = "Password@123"

        # Register
        driver.find_element(By.XPATH, "//input[@placeholder='email']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='password (min 6)']").send_keys(password)
        driver.find_element(By.XPATH, "//button[text()='Register']").click()

        # ✅ HANDLE ALERT
        time.sleep(1)
        alert = Alert(driver)
        alert.accept()

        time.sleep(1)

        # Login
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(2)

        # Assertion
        assert "Not logged in" not in driver.page_source

    finally:
        driver.quit()
