import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
import time
import psutil

# deprecated websites went here
NFTItemsPage = ""
NFTMintPage = ""
HuddlePage = ""

chromepath = r'/opt/homebrew/bin/chromedriver'

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(r'user-data-dir=/Users/kelvin/CS/Crypto/selenium/selenium_project/dailies')

service = Service(executable_path=chromepath)
driver = webdriver.Chrome(service=service, options=chrome_options)

print("Attempting to log into MetaMask...")
driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")

driver.delete_all_cookies()
actions = ActionChains(driver)

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
driver.get(NFTItemsPage)
blastr_window = driver.current_window_handle

time.sleep(10000)

def metamaskAcceptTxn():
    driver.switch_to.window(metamask_window)
    driver.refresh()
    time.sleep(5)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[3]/button[2]'))
    )
    confirm_mint_button = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[3]/button[2]')
    confirm_mint_button.click()
    driver.switch_to.window(blastr_window)

try:
    print("Refunding discovery pass...")
    #refund discovery pass
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div/div/div/div[3]'))
    )
    hover_element = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div/div/div/div[3]')
    actions.move_to_element(hover_element).perform()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div/div/div/div[4]/div/div[1]/button'))
    )
    refund_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[4]/div[2]/div/div/div/div/div/div/div/div[4]/div/div[1]/button')
    refund_button.click()

    time.sleep(2)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[16]/div[2]/div/div[4]/button'))
    )
    refund_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[16]/div[2]/div/div[4]/button')
    refund_button.click()

    time.sleep(2)

    print("Accepting txn...")
    metamaskAcceptTxn()

    driver.get(NFTMintPage)

    time.sleep(60)

    print("Boosting collection...")
    #boost
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[1]/div/div[2]/div/div[1]/div[2]/div/button'))
    )
    boost_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[1]/div/div[2]/div/div[1]/div[2]/div/button')
    boost_button.click()

    time.sleep(2)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[1]/button'))
    )
    expand_tab_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[1]/button')
    ariaExpanded =  expand_tab_button.get_attribute('aria-expanded');
    if expand_tab_button.get_attribute('aria-expanded') == 'false':
        expand_tab_button.click()

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[1]/div[2]/div/form/div/button'))
    )
    boost_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[1]/div[2]/div/form/div/button')
    boost_button.click()

    print("Accepting txn...")
    metamaskAcceptTxn()

    driver.get(NFTMintPage)

    time.sleep(60)

    print("Removing boost from collection...")
    #boost remove
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[1]/div/div[2]/div/div[1]/div[2]/div/button'))
    )
    boost_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div[3]/div[1]/div/div[2]/div/div[1]/div[2]/div/button')
    boost_button.click()

    time.sleep(2)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[2]/button'))
    )
    expand_tab_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[2]/button')
    ariaExpanded =  expand_tab_button.get_attribute('aria-expanded');
    if expand_tab_button.get_attribute('aria-expanded') == 'false':
        expand_tab_button.click()

    time.sleep(2)

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[2]/div[2]/div/button'))
    )
    boost_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[15]/div[2]/div/div[5]/div[2]/div[2]/div/button')
    boost_button.click()

    print("Accepting txn...")
    metamaskAcceptTxn()

    driver.get(NFTMintPage)
    time.sleep(60)

    print("Minting discovery pass...")

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.v-btn.v-theme--dark.bg-primary"))
    )
    mint_button = driver.find_elements(By.CSS_SELECTOR, "button.v-btn.v-theme--dark.bg-primary")

    mint_button[0].click()
    mint_button = driver.find_elements(By.CSS_SELECTOR, "button.v-btn.v-theme--dark.bg-primary")

    mint_button[3].click()

    print("Accepting txn...")
    metamaskAcceptTxn()

    print("Claiming Huddle dailies...")
    #huddle dailies
    driver.get(HuddlePage)
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/div/div[3]/div/div[6]/div[1]/dl/button'))
    )
    huddle_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[3]/div/div[6]/div[1]/dl/button')
    driver.execute_script("arguments[0].click();", huddle_button)
    time.sleep(2)

    print("Dailies completed!")

    driver.close()

except KeyboardInterrupt:
    driver.close()
