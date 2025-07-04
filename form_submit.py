import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/opt/chrome/chrome"

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("Navigating to URL...")
    driver.get("https://www.register2park.com/register?key=4wddrlcphom8")
    time.sleep(3)
    print("Page loaded. Attempting to fill form...")

    # Fill the form
    driver.find_element(By.NAME, "aptNumber").send_keys("1365")
    driver.find_element(By.NAME, "make").send_keys("BMW")
    driver.find_element(By.NAME, "model").send_keys("360i")
    driver.find_element(By.NAME, "licensePlate").send_keys("RBV6986")
    driver.find_element(By.NAME, "confirmLicensePlate").send_keys("RBV6986")
    print("Form fields filled. Clicking 'Next'...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

    print("Clicked 'Next'. Waiting for confirmation page...")
    time.sleep(10) # Increased sleep just in case the page takes longer to load

    # Construct the full path to save the screenshot
    screenshot_dir = os.environ.get('GITHUB_WORKSPACE', '.')
    screenshot_path = os.path.join(screenshot_dir, "confirmation.png")
    print(f"Attempting to save screenshot to: {screenshot_path}")

    driver.save_screenshot(screenshot_path)
    print(f"✅ Form submitted successfully and screenshot saved to: {screenshot_path}")

except Exception as e:
    print(f"❌ Error encountered: {e}")
    # Capture a screenshot even on error, if possible
    try:
        error_screenshot_path = os.path.join(os.environ.get('GITHUB_WORKSPACE', '.'), "error_screenshot.png")
        driver.save_screenshot(error_screenshot_path)
        print(f"Error screenshot saved to: {error_screenshot_path}")
    except Exception as se:
        print(f"Could not save error screenshot: {se}")
finally:
    print("Quitting WebDriver...")
    driver.quit()
    print("WebDriver quit.")
