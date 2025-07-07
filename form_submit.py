from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- Define Paths to Chrome and Chromedriver ---
CHROME_BINARY_PATH = './chrome-linux64/chrome'
CHROMEDRIVER_EXECUTABLE_PATH = './chromedriver-linux64/chromedriver'

# Set up Chrome options for headless mode and specify binary location
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1999,999")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--incognito")
chrome_options.binary_location = CHROME_BINARY_PATH

# Set up the Chromedriver service
service = Service(executable_path=CHROMEDRIVER_EXECUTABLE_PATH)

driver = None
try:
    print("Starting new navigation flow...")
    print(f"Attempting to launch Chrome with binary: {CHROME_BINARY_PATH}")
    print(f"Using ChromeDriver from: {CHROMEDRIVER_EXECUTABLE_PATH}")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # --- STEP 1: Navigate to base URL ---
    initial_url = "https://www.register2park.com/register"
    print(f"Navigating to initial URL: {initial_url}")
    driver.get(initial_url)
    time.sleep(3) # Give page time to load
    print(f"Actual URL after initial navigation: {driver.current_url}")
    
    # --- STEP 2: Type "capitol" and click 'next' ---
    print("Attempting to find property input field...")
    property_input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @type='search' or not(@type)]"))
    )
    property_input_field.send_keys("capitol")
    print("Typed 'capitol' into property field.")

    # Click the "Next" button (assuming its text is 'Next')
    next_button_step2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    next_button_step2.click()
    print("Clicked 'Next' after typing 'capitol'.")
    time.sleep(3) # Wait for results to load
    print(f"Actual URL after 'capitol' next: {driver.current_url}")

    # --- STEP 3: Click 'select' for 'capitol at stonebriar' ---
    print("Attempting to select 'capitol at stonebriar' using provided HTML.")
    # Using the precise data-property-id from the HTML you provided
    capitol_select_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-property-id='17001' and text()='Select']"))
    )
    capitol_select_button.click()
    print("Clicked 'Select' for 'capitol at stonebriar'.")
    time.sleep(3) # Wait for page to transition
    print(f"Actual URL after 'capitol at stonebriar' select: {driver.current_url}")

    # --- STEP 4: Click 'visitor parking' ---
    print("Attempting to click 'visitor parking'.")
    visitor_parking_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Visitor Parking')]"))
    )
    visitor_parking_button.click()
    print("Clicked 'Visitor Parking'.")
    time.sleep(5) # Give more time for the final form to load
    print(f"Actual URL after 'Visitor Parking' click: {driver.current_url}")

    # --- STEP 5: Fill out the form (now on https://www.register2park.com/register?key=4wddrlcphom8 implicitly) ---
    print("Reached form page. Attempting to fill form...")

    # Using By.ID with 'vehicleApt' for Apartment Number
    apt_number_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "vehicleApt"))
    )
    apt_number_field.send_keys("123")
    print("Filled 'Apartment Number'.")

    # Wait for and fill "Make" field (assuming 'name' attributes are correct)
    make_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "make"))
    )
    make_field.send_keys("Toyota")
    print("Filled 'Make'.")

    # Wait for and fill "Model" field (assuming 'name' attributes are correct)
    model_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "model"))
    )
    model_field.send_keys("Camry")
    print("Filled 'Model'.")

    # Wait for and fill "License Plate" field (assuming 'name' attributes are correct)
    license_plate_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "licensePlate"))
    )
    license_plate_field.send_keys("XYZ123")
    print("Filled 'License Plate'.")

    # Wait for and fill "Confirm License Plate" field (assuming 'name' attributes are correct)
    confirm_license_plate_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "confirmLicensePlate"))
    )
    confirm_license_plate_field.send_keys("XYZ123")
    print("Filled 'Confirm License Plate'.")

    # Click the "Next" button (for form submission)
    next_button_form = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    next_button_form.click()
    print("Clicked 'Next' to submit form.")

    # Give some time for the confirmation page to load
    time.sleep(5)

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
