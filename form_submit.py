from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/opt/chrome/chrome"

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

    time.sleep(5)

    # Save screenshot
   # ✅ Save screenshot to current directory
    driver.save_screenshot("./confirmation.png")
    print("✅ Form submitted successfully and screenshot saved!")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()
