import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
import time
import psutil

# deprecated sites went here
NFTMintPage = ""
NFTActivityPage = ""

chromepath = r'/opt/homebrew/bin/chromedriver'

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(r'user-data-dir=/Users/kelvin/CS/Crypto/selenium/selenium_project/anonanon')
chrome_options.add_argument('--disable-gpu')

# chrome_options.add_extension("./extensions/Metamask.crx")

service = Service(executable_path=chromepath)
driver = webdriver.Chrome(service=service, options=chrome_options)

print("Attempting to log into MetaMask...")
driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")

driver.delete_all_cookies()

metamask_window = driver.current_window_handle

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
)

input_element = driver.find_element(By.XPATH, '//*[@id="password"]')
input_element.send_keys("temporary" + Keys.ENTER)

print("Log in Successful.")
driver.switch_to.new_window('tab')
#enter the website
print("Opening Blastr...")
driver.get(NFTActivityPage)
blastr_window = driver.current_window_handle

# Record the start time when the program starts
start_time = time.time()
run_time = time.time()

print("Waiting to mint...")

# Function to write timestamp since the program started
def write_timestamp():
    # Calculate elapsed time since the program started
    elapsed_time = time.time() - start_time
    timestamp_message = f"Elapsed Time: {elapsed_time:.2f} seconds"

    # Write the timestamp to a file
    with open("timestamp_log.txt", "a") as file:
        file.write(timestamp_message)

    # Print the timestamp to the console (optional)
    print(timestamp_message)

def insert_to_cache(addr):
    refundAddrCache.append(addr)
    while len(refundAddrCache) > 10:
        refundAddrCache.pop()

def seconds_to_hhmmss(seconds):
    hours = seconds // 3600  # Get the total hours
    minutes = (seconds % 3600) // 60  # Get the remaining minutes
    remaining_seconds = seconds % 60  # Get the remaining seconds

    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"

def restart_browser(driver, chromepath, chrome_options):
    driver.quit()  # Close the existing browser session
    service = Service(executable_path=chromepath)
    return webdriver.Chrome(service=service, options=chrome_options)

previous_value = 0
current_value = 0
lastTxnAddr = "nothing"
refundAddrCache = []
restart_period = 2
try:
    while True:
        #restart every 2 hours
        if (time.time() - run_time > (restart_period * 3600)):  # Every 6 hours

            elapsed_time = time.time() - start_time
            print(f"Restart period of {restart_period} hours has elapsed")
            print("Elapsed Time: " + seconds_to_hhmmss(int(elapsed_time)) + " | Beginning retart...")
            # close all clients
            main_window = driver.current_window_handle
            window_handles = driver.window_handles

            # Switch to the MetaMask popup window
            for window in window_handles:
                if window != main_window:
                    driver.switch_to.window(window)
                    try:
                        # Close the popup window
                        driver.close()
                    except NoSuchWindowException:
                        print("Window already closed")
                    finally:
                        # Switch back to the main window
                        driver.switch_to.window(main_window)

            driver = restart_browser(driver, chromepath, chrome_options)
            print("Attempting to log into MetaMask...")
            driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
            driver.delete_all_cookies()

            metamask_window = driver.current_window_handle

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
            )

            input_element = driver.find_element(By.XPATH, '//*[@id="password"]')
            input_element.send_keys("temporary" + Keys.ENTER)

            print()
            driver.switch_to.new_window('tab')
            #enter the website
            print("Opening Blastr...")
            driver.get(NFTActivityPage)
            blastr_window = driver.current_window_handle
            run_time = time.time()  # Reset the timer
            elapsed_time = time.time() - start_time
            print("Elapsed Time: " + seconds_to_hhmmss(int(elapsed_time)) + " | Sucessfully restarted.")
            continue

        #get last transaction address
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div[1]/table/tbody/tr[1]/td[3]/a'))
            )
            WebDriverWait(driver, 1800).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div[1]/table/tbody/tr[1]/td[3]/a').text != lastTxnAddr
            )
        #just refresh the page if anything goes wrong
        except StaleElementReferenceException:
            driver.refresh()
            continue
        except TimeoutException:
            driver.refresh()
            continue

        #kind of pointless
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div[1]/table'))
        )

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//p[@class="pf-view-collection__funded-percent d-flex justify-space-between"]/span[2]'))
        )
        minted_info = driver.find_element(By.XPATH, '//p[@class="pf-view-collection__funded-percent d-flex justify-space-between"]/span[2]').text
        minted = int (minted_info.split("/")[0])
        #print("minted: " + str(minted))
        supply = int ((minted_info.split("/")[1]).split()[0])
        #print("supply: " + str(supply))
        minted_percentage = minted / supply

        #track transactions
        currTxnTypes = []
        currTxnAddrs = []
        table = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div[1]/table')
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
        try:
            for row in rows:
                txn_type = row.find_element(By.XPATH, './td[2]').text
                txn_addr = row.find_element(By.XPATH, './td[3]').text

                currTxnTypes.append(txn_type)
                currTxnAddrs.append(txn_addr)
        except StaleElementReferenceException:
            driver.refresh()
            continue

        # count number of refundTxns on current page
        refundTxnAddrs = [index for index, value in enumerate(currTxnTypes) if 'efund' in value]
        mintable = len(refundTxnAddrs)
        for index in refundTxnAddrs:
            if currTxnAddrs[index] in refundAddrCache:
                mintable = mintable - 1
                continue
            insert_to_cache(currTxnAddrs[index])

        # for row in rows:
        txnType = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div[1]/table/tbody/tr[1]/td[2]/span/div').text

        # print information nicely
        lastTxnAddr = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div[1]/table/tbody/tr[1]/td[3]/a').text
        elapsed_time = time.time() - start_time
        timestamp_message = f"Elapsed Time: {elapsed_time:.2f} seconds"
        print("Elapsed Time: " + seconds_to_hhmmss(int(elapsed_time)) + " | Txn: " +lastTxnAddr + " | Type: " + txnType)

        #temporary just for huddle, but also instance where the site was slow to update number of minted nfts
        if(mintable > 0 or minted_percentage < 1):
            print("Minting...")
            # attempt to mint
            driver.get(NFTMintPage)
            WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.v-btn.v-theme--dark.bg-primary"))
            )
            mint_button = driver.find_elements(By.CSS_SELECTOR, "button.v-btn.v-theme--dark.bg-primary")

            mint_button[0].click()
            mint_button = driver.find_elements(By.CSS_SELECTOR, "button.v-btn.v-theme--dark.bg-primary")

            mint_button[3].click()

            print("Swapping to MetaMask to confirm mint...")

            driver.switch_to.window(metamask_window)
            time.sleep(2)
            driver.refresh()
            time.sleep(5)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[3]/button[2]'))
            )
            confirm_mint_button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[3]/button[2]')
            confirm_mint_button.click()
            # try:
            #     WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[2]/div/div/div/div/div[1]/div'))
            # )
            #     confirm_mint_button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[2]/div/div/div/div/div[1]/div')
            #     confirm_mint_button.click()
            # except TimeoutException:
            #     pass
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]'))
            # )
            # confirm_mint_button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[3]/div[3]/footer/button[2]')
            # confirm_mint_button.click()
            driver.switch_to.window(blastr_window)
            print("Successfully minted! Waiting for next mint...")
            time.sleep(2)
            driver.get(NFTActivityPage)

    #delete the website afterwards
    # driver.quit()
except KeyboardInterrupt:
    driver.quit()
