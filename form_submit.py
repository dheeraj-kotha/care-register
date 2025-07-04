from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time # For time.sleep for demonstration, prefer WebDriverWait

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080") # Set a larger window size for consistent screenshots

# Path to chromedriver (assuming it's in the same directory or accessible via PATH)
# You might need to adjust this path based on where it's extracted
service = Service(executable_path='./chromedriver-linux64/chromedriver')

driver = None # Initialize driver to None
try:
    print("Navigating to URL...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://register2park.com/") # Replace with your actual URL
    print("Page loaded. Attempting to fill form...")

    # *** FIX: Use WebDriverWait to wait for the 'aptNumber' element ***
    # Wait for up to 10 seconds for the element with name "aptNumber" to be present
    apt_number_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Apartment Number:"))
    )
    apt_number_field.send_keys("123") # Replace "123" with the actual apartment number

    # You would repeat this WebDriverWait pattern for other fields if necessary
    make_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "make"))
    )
    make_field.send_keys("Toyota")

    model_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "model"))
    )
    model_field.send_keys("Camry")

    license_plate_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "licensePlate"))
    )
    license_plate_field.send_keys("XYZ123")

    confirm_license_plate_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "confirmLicensePlate"))
    )
    confirm_license_plate_field.send_keys("XYZ123")

    # Click the "Next" button
    # Wait for the button to be clickable
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']")) # Using XPath for button text
    )
    next_button.click()

    # Wait for a potential confirmation page to load and take a screenshot
    # Adjust this wait based on how long it takes for the confirmation page to appear
    time.sleep(3) # A short pause to ensure the next page has time to render

    # Take screenshot of the confirmation
    driver.save_screenshot("confirmation.png")
    print("Confirmation screenshot saved to: confirmation.png")

except Exception as e:
    print(f"❌ Error encountered: {e}")
    # Save a screenshot on error
    if driver: # Ensure driver is initialized before attempting to take screenshot
        driver.save_screenshot("error_screenshot.png")
        print("Error screenshot saved to: error_screenshot.png")
    print("For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#nosuchelementexception") # 
finally:
    if driver:
        print("Quitting WebDriver...")
        driver.quit()
        print("WebDriver quit.")
