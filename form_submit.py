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
# Ensure this path is correct for the GitHub Actions environment
chrome_options.binary_location = "/opt/chrome/chrome"

# Ensure this path is correct for the GitHub Actions environment
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.register2park.com/register?key=4wddrlcphom8")
    time.sleep(3)

    # Fill the form
    driver.find_element(By.NAME, "aptNumber").send_keys("1365")
    driver.find_element(By.NAME, "make").send_keys("BMW")
    driver.find_element(By.NAME, "model").send_keys("360i")
    driver.find_element(By.NAME, "licensePlate").send_keys("RBV6983")
    driver.find_element(By.NAME, "confirmLicensePlate").send_keys("RBV6983")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

    # Wait for the next page to load and content to be visible
    time.sleep(5)

    # Construct the full path to save the screenshot in the GitHub Actions workspace
    # This ensures the screenshot is saved where the upload-artifact action can find it.
    screenshot_path = os.path.join(os.environ.get('GITHUB_WORKSPACE', '.'), "confirmation.png")
    driver.save_screenshot(screenshot_path)
    print(f"✅ Form submitted successfully and screenshot saved to: {screenshot_path}")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()
