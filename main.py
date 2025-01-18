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

# Set localStorage item
def set_local_storage(driver, key, value):
    driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
    return driver.execute_script(f"return localStorage.getItem('{key}');")

# Add cookie to localStorage
def add_cookie_to_local_storage(driver, cookie):
    local_storage_items = {'B7S_AUTH_TOKEN': cookie}
    for key, value in local_storage_items.items():
        result = set_local_storage(driver, key, value)
        logging.info(f"Added {key} with value {result[:8]} to local storage.")

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

# Set Chrome storage item
def set_chrome_storage(driver, key, value):
    obj = {key: value}
    driver.execute_script(f"chrome.storage.local.set(JSON.parse('{json.dumps(obj)}'));")
    result = driver.execute_script(f"return chrome.storage.local.get('{key}');")
    return json.dumps(result[key])

# Add node key to Chrome storage
def add_node_keys_to_storage(driver, private_key, public_key, jwt_token):
    storage_items = {
        'authToken': jwt_token,
        'nodeData': {
            'peerEncryptedPrivKey': private_key,
            'peerPubKey': public_key
        }
    }
    for key, value in storage_items.items():
        result = set_chrome_storage(driver, key, value)
        logging.info(f"Added {key} with value {result[:8]} to storage.")

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

    version = '1.0.2'
    restart_delay = 60
    logging.info(f"Script version: {version}")

    try:
        os_info = get_os_info()
        logging.info(f"OS Info: {os_info}")

        # Read environment variables
        cookie = os.getenv('BLESS_AUTH_JWT')
        extension_id = os.getenv('EXTENSION_ID')
        extension_url = os.getenv('EXTENSION_URL')
        node_private_key = os.getenv('NODE_PRIVATE_KEY')
        node_public_key = os.getenv('NODE_PUBLIC_KEY')

        if not all([cookie, node_private_key, node_public_key]):
            logging.error("Missing required environment variables. Please set BLESS_AUTH_JWT, NODE_PRIVATE_KEY, and NODE_PUBLIC_KEY.")
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
        driver.set_window_size(1024, driver.get_window_size()['height'])
        logging.info("Accessing extension settings page...")
        driver.get(f"chrome-extension://{extension_id}/index.html")
        show_loading_animation(5)

        add_node_keys_to_storage(driver, node_private_key, node_public_key, cookie)
        logging.info("Token valid for 365 days. Update keys as necessary.")

        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        logging.info("Navigating to dashboard page...")
        driver.get(extension_url)

        while wait_for_element_exists(driver, By.XPATH, "//*[text()='Login']"):
            time.sleep(random.randint(3, 7))

        add_cookie_to_local_storage(driver, cookie)
        time.sleep(random.randint(3, 7))
        driver.refresh()

        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Dashboard']"):
            logging.info(f"Refreshing in {restart_delay} seconds to check login status.")
            time.sleep(restart_delay)

        logging.info("Switching back to extensions page...")
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Total Time']"):
            logging.info("Refreshing extension page...")
            time.sleep(random.randint(3, 7))
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
            connection_status(driver)
        except KeyboardInterrupt:
            logging.info('Stopping the script...')
            driver.quit()
            break

main()