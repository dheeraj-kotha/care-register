from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    # Open the form
    driver.get("https://www.register2park.com/register?key=4wddrlcphom8")

    # Fill the form
    driver.find_element(By.NAME, "aptNumber").send_keys("1365")
    driver.find_element(By.NAME, "make").send_keys("BMW")
    driver.find_element(By.NAME, "model").send_keys("360i")
    driver.find_element(By.NAME, "licensePlate").send_keys("RBV6983")
    driver.find_element(By.NAME, "confirmLicensePlate").send_keys("RBV6983")

    # Click the "Next" button
    driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

    # Wait for confirmation page to load
    time.sleep(5)  # adjust if needed for slower page load

    # Take a screenshot
    driver.save_screenshot("confirmation.png")
    print("✅ Form submitted and screenshot saved.")

finally:
    driver.quit()
