import os
import time
import sys
import yaml
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Driver constants
chromedriver_path = "C:\\SeleniumWebDrivers\\Windows\\chromedriver.exe"
chrome_options = Options() 
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--window-size=1920x1080")
screeenshots_directory = "..\_TestScreenshots"
reports_directory = "..\_TestReports"

# Read parameters from Yaml file
parameters = open("..\data.yml")
info = yaml.load(parameters)
user_name = info['UserName']
user_password = info['UserPassword']
new_client_name = info['NewClientName']
headless_mode = info['HeadlessMode']

################################################## FUNCTIONS SECTION ##################################################
def SystemLogin(driver):
    # Navigate to Onboarding page
    driver.get("https://alliedglobalonboarding.azurewebsites.net/")
    driver.maximize_window()
    driver.implicitly_wait(30)
    wait = WebDriverWait(driver, 10)

    # Write Email
    wait.until(EC.presence_of_element_located((By.ID, 'i0116')))
    email_text = driver.find_element_by_xpath('//*[@id="i0116"]')
    email_text.send_keys(user_name)

    # Click on Next
    next_button = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    next_button.click()

    # Select Account Type
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aadTitleHint"]/small')))
    account_type = driver.find_element_by_xpath('//*[@id="aadTitleHint"]/small')
    account_type.click()

    # Write Password
    wait.until(EC.presence_of_element_located((By.ID, "i0118")))
    password_text = driver.find_element_by_xpath('//*[@id="i0118"]')
    password_text.send_keys(user_password)

    # Click on Sign in
    signin_button = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    signin_button.click()

    # Click on Yes
    wait.until(EC.presence_of_element_located((By.ID, "idSIButton9")))
    yes_button = driver.find_element_by_xpath('//*[@id="idSIButton9"]')
    yes_button.click()
    
    return driver

################################################## TEST CLASS ##################################################
class TestLogin(unittest.TestCase):
    # SetUp function
    def setUp(self):
        # Create WebDriver
        driver = {}
        if(headless_mode == True):
            driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
            driver.set_page_load_timeout(120)
        else:
            driver = webdriver.Chrome(executable_path=chromedriver_path)
            driver.set_page_load_timeout(120)
        
        # Create folder for screenshots
        if not os.path.exists(screeenshots_directory):
            os.makedirs(screeenshots_directory)
        
        # Create folder for reports
        if not os.path.exists(reports_directory):
            os.makedirs(reports_directory)

        # Create self driver
        self.driver = driver
    
    # Test login test case
    def test_system_login(self):
        driver = self.driver
        
        # System Login
        driver = SystemLogin(self.driver)
        wait = WebDriverWait(driver, 10)

        # Get username logged
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div[2]/ul[2]/li[1]")))
        user_name_label = driver.find_element_by_xpath('/html/body/nav/div/div[2]/ul[2]/li[1]')

        # Assert of username logged
        try: 
            assert user_name_label.text == 'Hello ' + user_name + '!'
            driver.get_screenshot_as_file(screeenshots_directory + "\login.png")
            print('User successfully logged.')
        except AssertionError as error:
            driver.get_screenshot_as_file(screeenshots_directory + "\login-error.png")
            print("Username assert failed!")
            print("Found value is: " + user_name.text)
    
    # Client creation test case
    def test_create_client(self):
        driver = self.driver
        
        # System Login
        driver = SystemLogin(self.driver)
        wait = WebDriverWait(driver, 10)

        # Click on Clients Menu
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/div[2]/ul[1]/li/a')))
        clients_menu = driver.find_element_by_xpath('/html/body/nav/div/div[2]/ul[1]/li/a')
        clients_menu.click()

        # Click on Create New button
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/p/a')))
        create_new_button = driver.find_element_by_xpath('/html/body/div/p/a')
        create_new_button.click()

        # Enter new client name
        wait.until(EC.presence_of_element_located((By.ID, 'Name')))
        new_client_text = driver.find_element_by_id('Name')
        new_client_text.send_keys(new_client_name)

        # Click on Create button
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/form/div[2]/input')))
        create_button = driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div[2]/input')
        create_button.click()

        # Assert client exists
        try:
            assert EC.presence_of_element_located((By.XPATH, '/html/body/div/table/tbody')) == True
        except AssertionError as error:
            driver.get_screenshot_as_file(screeenshots_directory + "\createclient-exists.png")
            print("Client already exists!")

        clients_table = driver.find_element_by_xpath('/html/body/div/table/tbody')
        clients_table_rows = clients_table.find_elements_by_xpath('tr')

        # Search on table the name of the client
        client_exists = False
        for x in clients_table_rows:
            client_name = x.find_element_by_xpath('td[1]')
            if(client_name.text == new_client_name):
                client_exists = True
                break
        
        # Assert client created
        try:  
            assert client_exists == True
            driver.get_screenshot_as_file(screeenshots_directory + "\createclient.png")
            print("Client successfully created.")
        except AssertionError as error:
            driver.get_screenshot_as_file(screeenshots_directory + "\createclient-error.png")
            print("Client was not created.")

    # End process function
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    # unittest.main()
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=reports_directory))