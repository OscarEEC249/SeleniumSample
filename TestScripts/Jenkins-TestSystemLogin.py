import os
import shutil
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
from selenium.common.exceptions import TimeoutException

# Driver constants
chromedriver_path = "/usr/bin/chromedriver"
chrome_options = Options() 
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--window-size=1920x1080")

# Read parameters from Yaml files
parameters = open("./data-jenkins.yml")
info = yaml.load(parameters)
screeenshots_directory = info['ScreenshotsDirectory']
reports_directory = info['ReportsDirectory']
user_name = info['UserName']
user_password = info['UserPassword']
new_client_name = info['NewClientName']
headless_mode = info['HeadlessMode']

################################################## FUNCTIONS SECTION ##################################################
def SystemLogin(driver):
    try:
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

        # # Select Account Type
        # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="aadTitleHint"]/small')))
        # account_type = driver.find_element_by_xpath('//*[@id="aadTitleHint"]/small')
        # account_type.click()

        # Write Password
        time.sleep(1)
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
    except selenium.common.exceptions.TimeoutException:
        driver.get_screenshot_as_file(screeenshots_directory + "\login-error.png")
        print("Login failed!")
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

################################################## TEST CLASS ##################################################
class TestSystemDemo(unittest.TestCase):
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
        try:
            driver = self.driver
            
            # System Login
            driver = SystemLogin(self.driver)
            wait = WebDriverWait(driver, 10)

            # Get username logged
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div[2]/ul[2]/li[1]")))
            user_name_label = driver.find_element_by_xpath('/html/body/nav/div/div[2]/ul[2]/li[1]')

            # Assert of username logged
            assert user_name_label.text == 'Hello ' + user_name + '!'
            driver.get_screenshot_as_file(screeenshots_directory + "login.png")
            
        except AssertionError:
            driver.get_screenshot_as_file(screeenshots_directory + "login-error.png")
            print("Login failed!")
            raise
        except TimeoutException:
            driver.get_screenshot_as_file(screeenshots_directory + "login-error.png")
            print("Login failed!")
            raise
        except:
            driver.get_screenshot_as_file(screeenshots_directory + "login-error.png")
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # End process function
    def tearDown(self):
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=reports_directory))
