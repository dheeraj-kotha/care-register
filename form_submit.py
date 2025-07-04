from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/google-chrome"  # Required for GitHub Actions

# Point to the correct Chromedriver path
service = Service("/usr/bin/chromedriver")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the Register2Park form with key
    driver.get("https://www.register2park.com/register?key=4wddrlcphom8")

    # Wait for the page to fully load
    time.sleep(3)

     # Fill the form
    driver.find_element(By.NAME, "aptNumber").send_keys("1365")
    driver.find_element(By.NAME, "make").send_keys("BMW")
    driver.find_element(By.NAME, "model").send_keys("360i")
    driver.find_element(By.NAME, "licensePlate").send_keys("RBV6983")
    driver.find_element(By.NAME, "confirmLicensePlate").send_keys("RBV6983")


    # Submit the form
    driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]").click()

    # Wait for confirmation page to load
    time.sleep(5)

    # Take a screenshot of the success page
    driver.save_screenshot("confirmation.png")
    print("✅ Form submitted successfully and screenshot saved as confirmation.png.")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    driver.quit()
