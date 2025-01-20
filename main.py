import os
import distro
import platform
import subprocess
import random
import time
import logging
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging configuration
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Display CLI loading animation
def show_loading_animation(duration):
    random
    for _ in range(duration):
        for frame in "|/-\\":
            print(f"\rLoading... {frame}", end="", flush=True)
            time.sleep(0.2)
    print("\r", end="")

# Check connection status
def check_connection_status(driver):
    if wait_for_element_exists(driver, By.XPATH, "//*[text()='Online']"):
        logging.info("Status: Online!")
    elif wait_for_element_exists(driver, By.XPATH, "//*[text()='Offline']"):
        logging.warning("Status: Disconnected!")
    else:
        logging.warning("Status: Unknown!")

# Wait for an element to exist
def wait_for_element_exists(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return True
    except TimeoutException:
        return False


# Wait for an element to be present
def wait_for_element(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException as e:
        logging.error(f"Error waiting for element {value}: {e}")
        raise

# Get ChromeDriver version
def get_chromedriver_version():
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Could not get ChromeDriver version: {e}")
        return "Unknown version"

# Get OS information
def get_os_info():
    try:
        os_info = {'System': platform.system(), 'Version': platform.version()}
        if os_info['System'] == 'Linux':
            os_info.update({
                'System': distro.name(pretty=True),
                'Version': distro.version(pretty=True, best=True)
            })
        return os_info
    except Exception as e:
        logging.error(f"Could not get OS information: {e}")
        return "Unknown OS"

# Main execution function
def main():
    setup_logging()

    version = '1.0.6'
    restart_delay = 60
    logging.info(f"Script version: {version}")

    try:
        os_info = get_os_info()
        logging.info(f"OS Info: {os_info}")

        # Read environment variables
        extension_id = os.getenv('EXTENSION_ID')
        web_url = os.getenv('WEB_URL')
        
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        if not all([email, password]):
            logging.error("Missing required environment variables. Please set EMAIL, PASSWORD.")
            return

        chrome_options = Options()
        chrome_options.add_extension(f"./{extension_id}.crx")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0")

        # Initialize WebDriver
        chromedriver_version = get_chromedriver_version()
        logging.info(f"Using ChromeDriver: {chromedriver_version}")
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        logging.error(f"Restarting in {restart_delay} seconds...")
        time.sleep(restart_delay)
        main()
        return

    try:
        # logins
        driver.set_window_size(1024, driver.get_window_size()['height'])
        logging.info("Accessing spark dashboard page...")
        driver.get(web_url)
        
        show_loading_animation(random.randint(1, 3))
        
        while wait_for_element_exists(driver, By.XPATH, "//*[text()='Login']"):
            show_loading_animation(random.randint(1, 3))
            
        logging.info("Login...")
        
        logging.info('Entering credentials...')
        email_em = browser.find_element(By.XPATH, "//input[contains(@placeholder,'Email')]")

        email_em.send_keys(email)
        passworld_em = browser.find_element(By.XPATH, "//input[contains(@placeholder,'Password')]")
        passworld_em.send_keys(password)
        
        logging.info('Clicking the login button...')
        login_em = driver.find_element(By.XPATH, "//button[text()='Login']")
        login_em.click()
        logging.info('Waiting response...')

        while wait_for_element_exists(driver, By.XPATH, "//*[text()='Dashboard']"):
            show_loading_animation(random.randint(1, 3))

        show_loading_animation(random.randint(1, 3))
        logging.info('Accessing extension page...')
        driver.get(f'chrome-extension://{extension_id}/popup.html')
        
        while wait_for_element_exists(driver, By.XPATH, "//*[text()='Login']"):
            show_loading_animation(random.randint(1, 3))
        
        logging.info('Login Extension...')
        button = driver.find_element(By.XPATH, "//*[text()='Login']")
        button.click()


        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Epoch Earnings:']"):
            logging.info("Refreshing extension page...")
            show_loading_animation(random.randint(1, 3))
            driver.refresh()

        # Get handles for all windows
        all_windows = driver.window_handles

        # Get the handle of the active window
        active_window = driver.current_window_handle

        # Close all windows except the active one
        for window in all_windows:
            if window != active_window:
                driver.switch_to.window(window)
                driver.close()

        # Switch back to the active window
        driver.switch_to.window(active_window)

        check_connection_status(driver)
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        logging.error(f'Restarting in {restart_delay} seconds...')
        driver.quit()
        time.sleep(restart_delay)
        main()

    while True:
        try:
            time.sleep(3600)
            driver.refresh()
            check_connection_status(driver)
        except KeyboardInterrupt:
            logging.info('Stopping the script...')
            driver.quit()
            break

main()