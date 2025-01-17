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

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connection_status(driver):
    if wait_for_element_exists(driver, By.XPATH, "//*[text()='Online']"):
        logging.info("Status: Online!")
    elif wait_for_element_exists(driver, By.XPATH, "//*[text()='Offline']"):
        logging.warning("Status: Disconnected!")
    else:
        logging.warning("Status: Unknown!")

def set_local_storage_item(driver, key, value):
    driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
    result = driver.execute_script(f"return localStorage.getItem('{key}');")
    return result

def add_cookie_to_local_storage(driver, cookie_value):
    local_storage_items = {
        'B7S_AUTH_TOKEN': cookie_value
    }
        
    for key, value in local_storage_items.items():
        result = set_local_storage_item(driver, key, cookie_value)
        logging.info(f"Added {key} with value {result[:8]} to local storage.")

def wait_for_element_exists(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return True
    except TimeoutException:
        return False

def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException as e:
        logging.error(f"Error waiting for element {value}: {e}")
        raise

def set_chrome_storage_item(driver, key, value):
    obj = {
        f'{key}': value
    }
    
    driver.execute_script(f"chrome.storage.local.set(JSON.parse('{json.dumps(obj)}'));")
    result = driver.execute_script(f"return chrome.storage.local.get('{key}');")
    return json.dumps(result[key])
    
def add_node_key_to_chrome_storage(driver, priv_key, pub_key, jwt_cookie):
    local_storage_items = {
        'authToken':jwt_cookie, 
        'nodeData':  {
            'peerEncryptedPrivKey': priv_key,
            'peerPubKey': pub_key
        }
    }
    
    for key, value in local_storage_items.items():
        result = set_chrome_storage_item(driver, key, value)
        logging.info(f"Added {key} with value {result[:8]} to local storage.")
        
def get_chromedriver_version():
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Could not get ChromeDriver version: {e}")
        return "Unknown version"

def get_os_info():
    try:
        os_info = {
            'System': platform.system(),
            'Version': platform.version()
        }
        
        if os_info['System'] == 'Linux':
            os_info.update({
                'System': distro.name(pretty=True),
                'Version': distro.version(pretty=True, best=True)
            })
        return os_info
    except Exception as e:
        logging.error(f"Could not get OS information: {e}")
        return "Unknown OS"

def run():
    setup_logging()
    
    branch = ''
    version = '1.0.1' + branch
    secUntilRestart = 60
    logging.info(f"Started the script {version}")

    try:
        os_info = get_os_info()
        logging.info(f'OS Info: {os_info}')
        
        # Read variables from the OS env
        cookie = os.getenv('BLESS_COOKIE')
        extension_id = os.getenv('EXTENSION_ID')
        extension_url = os.getenv('EXTENSION_URL')


        node_private_key = os.getenv('NODE_PRIV_KEY')
        node_public_key = os.getenv('NODE_PUB_KEY')
        # Check if credentials are provided
        if not cookie:
            logging.error('No cookie provided. Please set the BLESS_COOKIE environment variable.')
            return  # Exit the script if credentials are not provided

        if not node_private_key:
            logging.error('No cookie provided. Please set the NODE_PRIV_KEY environment variable.')
            return  # Exit the script if credentials are not provided
        if not node_public_key:
            logging.error('No cookie provided. Please set the NODE_PUB_KEY environment variable.')
            return  # Exit the script if credentials are not provided

        chrome_options = Options()
        chrome_options.add_extension(f'./{extension_id}.crx')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0")

        # Initialize the WebDriver
        chromedriver_version = get_chromedriver_version()
        logging.info(f'Using {chromedriver_version}')
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        logging.error(f'Restarting in 60 seconds...')
        time.sleep(secUntilRestart)
        run()

    try:
        # NodePass checks for width less than 1024p
        driver.set_window_size(1024, driver.get_window_size()['height'])

        logging.info('Accessing extension settings page...')
        driver.get(f'chrome-extension://{extension_id}/index.html')
      
            
        time.sleep(random.randint(3,7))
    
            
        add_node_key_to_chrome_storage(driver, node_private_key, node_public_key, cookie)
        logging.info("!!!!! Your token can be used to login for 365 days !!!!!")
        logging.info("!!!!! Update Node Private/Public key when you retire it !!!!!")
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        
        logging.info('Get into dashboard page...')
        driver.get(extension_url)
        while wait_for_element_exists(driver, By.XPATH, "//*[text()='Login']"):
            time.sleep(random.randint(3,7))
            
        logging.info('Add cookie to dashboard page ...')
        # add cookies 
        add_cookie_to_local_storage(driver, cookie)
        
        time.sleep(random.randint(3,7))
        
        driver.refresh()
        # wait for dashboard 
        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Dashboard']"):
            logging.info(f'Refreshing in {secUntilRestart} seconds to check login (If stuck, verify your token)...')
        
        logging.info('Refresh Extensions page...')
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        
        
        # Refresh until the page can accessiable
        while not wait_for_element_exists(driver, By.XPATH, "//*[text()='Total Time']"):
            time.sleep(random.randint(3,7))
            # Refresh the page
            logging.info('Refresh...')
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

        connection_status(driver)
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        logging.error(f'Restarting in {secUntilRestart} seconds...')
        driver.quit()
        time.sleep(secUntilRestart)
        run()

    while True:
        try:
            time.sleep(3600)
            driver.refresh()
            connection_status(driver)
        except KeyboardInterrupt:
            logging.info('Stopping the script...')
            driver.quit()
            break

run()
