import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import platform

@pytest.fixture(scope="module")
def driver():
    # Setup Firefox WebDriver with automatic Firefox binary location detection
    options = FirefoxOptions()
    options.headless = True  
    # No need to manually specify the Firefox binary location, it should be found automatically
    if platform.system() == "Windows":
        # Optional: You can specify the path here if it's not in the default location
        pass
    elif platform.system() == "Darwin":  # macOS
        # Firefox should be automatically found on macOS without setting the binary location
        pass
    elif platform.system() == "Linux":
        # Firefox should be automatically found on Linux without setting the binary location
        pass
    
    # Using GeckoDriverManager to automatically manage Firefox and GeckoDriver binaries
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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-username")))
    driver.find_element(By.ID, "user-username").send_keys("newuser")
    driver.find_element(By.ID, "user-password").send_keys("newpassword")
    driver.find_element(By.ID, "form-submit").click()
    
    # Check if redirected to the home page
    assert driver.current_url == "http://localhost:5000/"

def test_logout(driver):
    driver.get("http://localhost:5000/")
    
    # Click the logout link
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Logout")))
    driver.find_element(By.LINK_TEXT, "Logout").click()
    
    # Check if redirected to the login page
    assert driver.current_url == "http://localhost:5000/login"
