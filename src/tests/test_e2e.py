import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

import pytest
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope="module")
def driver():
    # Setup Firefox WebDriver with OS-specific binary location
    options = FirefoxOptions()
    if platform.system() == "Windows":
        options.binary_location = r"C:\Users\po44oov\AppData\Local\Mozilla Firefox\firefox.exe"  # Adjust if necessary
    elif platform.system() == "Darwin":  # macOS
        options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
    elif platform.system() == "Linux":
        options.binary_location = "/usr/bin/firefox"  # Adjust for Linux if necessary
    
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_register(driver):
    driver.get("http://localhost:5000/register")
    
    # Generate a unique username
    import time
    unique_username = f"newuser{int(time.time())}"
    
    # Fill out the registration form
    driver.find_element(By.NAME, "username").send_keys(unique_username)
    driver.find_element(By.NAME, "email").send_keys(f"{unique_username}@example.com")
    driver.find_element(By.NAME, "password").send_keys("newpassword")
    driver.find_element(By.NAME, "confirm-password").send_keys("newpassword")
    driver.find_element(By.ID, "form-submit").click()
    
    # Check if redirected to the home page
    current_url = driver.current_url
    if current_url != "http://localhost:5000/":
        print("Current URL:", current_url)
        print("Page source:")
        print(driver.page_source)  # Debugging line to print the page source if the URL is not as expected
    assert current_url == "http://localhost:5000/"

def test_login(driver):
    driver.get("http://localhost:5000/login")
    
    # Fill out the login form
    driver.find_element(By.NAME, "username").send_keys("newuser")
    driver.find_element(By.NAME, "password").send_keys("newpassword")
    driver.find_element(By.ID, "form-submit").click()
    
    # Check if redirected to the home page
    assert driver.current_url == "http://localhost:5000/"

def test_logout(driver):
    driver.get("http://localhost:5000/")
    
    # Click the logout link
    driver.find_element(By.LINK_TEXT, "Logout").click()
    
    # Check if redirected to the login page
    assert driver.current_url == "http://localhost:5000/login"