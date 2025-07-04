from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless=new")
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

    # Wait until either confirmation or error element loads (max 10 seconds)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Confirmation')]"))
    )

    # ✅ Screenshot page after successful submission
    driver.save_screenshot("confirmation.png")
    print("✅ Screenshot captured after submission.")

except Exception as e:
    print(f"❌ Error during form submission or screenshot: {e}")

finally:
    driver.quit()
