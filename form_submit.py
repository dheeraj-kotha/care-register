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
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu") # May help on some systems or with certain rendering detections
chrome_options.add_argument("--disable-extensions") # Disable browser extensions
chrome_options.add_argument("--no-first-run") # Suppress first-run dialogs
chrome_options.add_argument("--no-default-browser-check") # Suppress default browser check
chrome_options.add_argument("--incognito") # Start in incognito mode (clean session)
chrome_options.binary_location = CHROME_BINARY_PATH # Tell Selenium where to find the Chrome binary

# Set up the Chromedriver service
service = Service(executable_path=CHROMEDRIVER_EXECUTABLE_PATH)

driver = None
try:
    print("Navigating to URL...")
    print(f"Attempting to launch Chrome with binary: {CHROME_BINARY_PATH}")
    print(f"Using ChromeDriver from: {CHROMEDRIVER_EXECUTABLE_PATH}")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    target_url = "https://www.register2park.com/register" # Store target URL
    driver.get(target_url)
    print(f"Requested URL: {target_url}") # Log requested URL
    time.sleep(2) # Give a moment for any redirects to complete
    print(f"Actual URL after navigation: {driver.current_url}") # Log actual current URL

    # Check if the actual URL matches the expected URL
    if driver.current_url != target_url:
        print(f"Warning: Browser redirected from {target_url} to {driver.current_url}")
        # Take an immediate screenshot if redirection occurs
        redirect_screenshot_name = "redirect_screenshot.png"
        driver.save_screenshot(redirect_screenshot_name)
        print(f"Screenshot of redirected page saved to: {redirect_screenshot_name}")


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
