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
# This path is correct for the setup in your GitHub Actions workflow
chrome_options.binary_location = "/opt/chrome/chrome"

# This path is correct for the setup in your GitHub Actions workflow
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
    # Give it more time, or ideally, use an explicit wait for a specific element on the confirmation page
    time.sleep(10)

    # Construct the full path to save the screenshot in the GitHub Actions workspace
    # GITHUB_WORKSPACE is the default working directory, so '.' should also work if script is in root.
    # However, explicitly using os.getcwd() here will confirm the script's current directory.
    screenshot_dir = os.getcwd() # Get current working directory of the script
    screenshot_path = os.path.join(screenshot_dir, "confirmation.png")
    print(f"Attempting to save screenshot to: {screenshot_path}")

    driver.save_screenshot(screenshot_path)
    print(f"✅ Form submitted successfully and screenshot saved to: {screenshot_path}")

except Exception as e:
    print(f"❌ Error encountered: {e}")
    # Capture a screenshot even on error, if possible
    try:
        error_screenshot_path = os.path.join(os.getcwd(), "error_screenshot.png")
        driver.save_screenshot(error_screenshot_path)
        print(f"Error screenshot saved to: {error_screenshot_path}")
    except Exception as se:
        print(f"Could not save error screenshot: {se}")
finally:
    print("Quitting WebDriver...")
    driver.quit()
    print("WebDriver quit.")
