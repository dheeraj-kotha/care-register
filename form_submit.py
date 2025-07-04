from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- Define Paths to Chrome and Chromedriver ---
# These paths are relative to where your script runs inside GitHub Actions.
# They point to the executables inside the folders that will be extracted
# by your GitHub Actions workflow.
CHROME_BINARY_PATH = './chrome-linux64/chrome'
CHROMEDRIVER_EXECUTABLE_PATH = './chromedriver-linux64/chromedriver'

# Set up Chrome options for headless mode and specify binary location
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless") # Runs Chrome without a UI
chrome_options.add_argument("--no-sandbox") # Required for some Linux environments like GitHub Actions
chrome_options.add_argument("--disable-dev-shm-usage") # Overcomes limited resource problems
chrome_options.add_argument("--window-size=1920,1080") # Set a consistent window size
chrome_options.binary_location = CHROME_BINARY_PATH # Tell Selenium where to find the Chrome binary

# Set up the Chromedriver service
service = Service(executable_path=CHROMEDRIVER_EXECUTABLE_PATH)

driver = None
try:
    print("Navigating to URL...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.register2park.com/register?key=4wddrlcphom8") # Replace with your actual URL
    print("Page loaded. Attempting to fill form...")

    # Wait for the "Apartment Number" field
    apt_number_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "vehicleApt"))
    )
    apt_number_field.send_keys("123") # Replace "123" with the actual apartment number

    # Wait for and fill "Make" field
    make_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "vehicleMake"))
    )
    make_field.send_keys("Toyota")

    # Wait for and fill "Model" field
    model_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "vehicleModel"))
    )
    model_field.send_keys("Camry")

    # Wait for and fill "License Plate" field
    license_plate_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "vehicleLicensePlate"))
    )
    license_plate_field.send_keys("XYZ123")

    # Wait for and fill "Confirm License Plate" field
    confirm_license_plate_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "vehicleLicensePlateConfirm"))
    )
    confirm_license_plate_field.send_keys("XYZ123")

    # Click the "Next" button
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    next_button.click()

    # Give some time for the next page/confirmation to load
    time.sleep(5) # You might need to adjust this depending on page load speed

    # Take screenshot of the confirmation page
    screenshot_name = "confirmation.png"
    driver.save_screenshot(screenshot_name)
    print(f"Confirmation screenshot saved to: {screenshot_name}")

except Exception as e:
    print(f"❌ Error encountered: {e}")
    # Save a screenshot on error
    if driver:
        error_screenshot_name = "error_screenshot.png"
        driver.save_screenshot(error_screenshot_name)
        print(f"Error screenshot saved to: {error_screenshot_name}")
    print("For documentation on Selenium errors, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/")
finally:
    if driver:
        print("Quitting WebDriver...")
        driver.quit()
        print("WebDriver quit.")
