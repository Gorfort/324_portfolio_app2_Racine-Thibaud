import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import platform
import time

@pytest.fixture(scope="module")
def driver():
    # Setup Firefox WebDriver with automatic Firefox binary location detection
    options = FirefoxOptions()
    options.headless = True  # Run headless, or set to False if you want a visible browser window
    
    # Using GeckoDriverManager to automatically manage Firefox and GeckoDriver binaries
    driver_path = GeckoDriverManager().install()
    driver = webdriver.Firefox(executable_path=driver_path, options=options)
    
    driver.implicitly_wait(10)  # Set implicit wait time for elements to load
    yield driver  # Yield the driver to be used in tests
    driver.quit()  # Cleanup after tests are done

def test_register(driver):
    driver.get("http://localhost:5000/register")
    
    # Generate a unique username based on the current timestamp
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
        print(driver.page_source)  # For debugging if URL is not expected
    assert current_url == "http://localhost:5000/"

def test_login(driver):
    driver.get("http://localhost:5000/login")
    
    # Wait until the username field is present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-username")))
    
    # Fill out the login form
    driver.find_element(By.ID, "user-username").send_keys("newuser")
    driver.find_element(By.ID, "user-password").send_keys("newpassword")
    driver.find_element(By.ID, "form-submit").click()
    
    # Check if redirected to the home page after login
    assert driver.current_url == "http://localhost:5000/"

def test_logout(driver):
    driver.get("http://localhost:5000/")
    
    # Wait for the logout link to be clickable
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    
    # Click the logout link
    driver.find_element(By.LINK_TEXT, "Logout").click()
    
    # Check if redirected to the login page after logout
    assert driver.current_url == "http://localhost:5000/login"
