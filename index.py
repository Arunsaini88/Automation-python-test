import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
import time
import requests
import os
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("selenium_test.log"),
    logging.StreamHandler()
])

# Initialize the WebDriver
# driver_path = "/path/to/chromedriver"  # Replace with the actual path if not in PATH
driver = webdriver.Chrome()

# 1. Open the website
url = "https://atg.party"
logging.info(f"Opening website: {url}")
start_time = time.time()
driver.get(url)
load_time = time.time() - start_time
logging.info(f"Page load time: {load_time} seconds")

# 2. Check the HTTP response code
response = requests.get(url)
logging.info(f"HTTP response code: {response.status_code}")

# 3. Click on the LOGIN button and use the provided credentials
try:
    logging.info("Clicking on LOGIN button")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "login-link"))
    )
    login_button.click()
except (NoSuchElementException, TimeoutException) as e:
    logging.error("Login button not found or not clickable. Exiting. Error: %s", e)
    driver.quit()
    exit()

# Wait for the login form to appear
try:
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "email_landing"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "password_landing"))
    )
    email_input.send_keys("wiz_saurabh@rediffmail.com")
    password_input.send_keys("Pass@123")

    login_submit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "landing-signin-btn"))
    )
    login_submit.click()
    logging.info("Logged in successfully")
except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
    logging.error("Error during login process. Exiting. Error: %s", e)
    driver.quit()
    exit()

# 4. Click on the Create button
try:
    create_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "create-btn-dropdown"))
    )
    create_button.click()
    logging.info("Clicked on Create button")
except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
    logging.error("Create button not found or not clickable. Exiting. Error: %s", e)
    driver.quit()
    exit()

# 5. Navigate to the URL: atg.party/article
article_url = "https://atg.party/article"
logging.info(f"Navigating to: {article_url}")
driver.get(article_url)

# 6. Fill in the title and description
try:
    title_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "title"))
    )
    description_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ce-paragraph[data-placeholder-active]"))
    )
    title_input.send_keys("Sample Title")
    description_input.send_keys("Sample description for the article.")
    logging.info("Filled in the title and description")
except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
    logging.error("Error during filling in the title and description. Exiting. Error: %s", e)
    driver.quit()
    exit()

# 7. Upload a cover image
try:
    # Get the absolute path to the image file in the current working directory
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "images", "Screenshot (1).png")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at path: {image_path}")

    cover_image_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cover_image"))
    )
    cover_image_input.send_keys(image_path)
    logging.info(f"Uploaded cover image from path: {image_path}")
except (NoSuchElementException, TimeoutException) as e:
    logging.error("Error during uploading cover image. Exiting. Error: %s", e)
    driver.quit()
    exit()
except FileNotFoundError as e:
    logging.error(e)
    driver.quit()
    exit()

# 8. Click on the POST button
try:
    post_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hpost_btn"))
    )
    post_button.click()
    logging.info("Clicked on POST button")
except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:
    logging.error("Error during clicking POST button. Exiting. Error: %s", e)
    driver.quit()
    exit()

# 9. Log the URL of the new page
time.sleep(5)  # wait for the page to load
new_page_url = driver.current_url
logging.info(f"New article URL: {new_page_url}")

# Close the browser
driver.quit()
logging.info("Browser closed")
