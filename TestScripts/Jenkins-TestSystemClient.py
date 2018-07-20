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
from selenium.webdriver.common.action_chains import ActionChains

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
new_client_project = info['NewClientProject']
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

    # Client creation test case
    def test_create_client_project(self):
        try:
            driver = self.driver
            
            # System Login
            driver = SystemLogin(self.driver)
            wait = WebDriverWait(driver, 10)

            # Click on Clients Menu
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/div[2]/ul[1]/li/a')))
            clients_menu = driver.find_element_by_xpath('/html/body/nav/div/div[2]/ul[1]/li/a')
            clients_menu.click()

            # Wait until Clients table appears
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/table/tbody')))
            clients_table = driver.find_element_by_xpath('/html/body/div/table/tbody')
            clients_table_rows = clients_table.find_elements_by_xpath('tr')

            # Search on table the name of the client
            client_manage_project = ""
            for x in clients_table_rows:
                client_name = x.find_element_by_xpath('td[1]')
                if(client_name.text == new_client_name):
                    # Save the object to click and create project
                    client_manage_project = x.find_element_by_xpath('td[4]').find_element_by_xpath('a[2]')
                    break
            
            # Click on Manage Projects
            client_manage_project.click()

            # Click on Create new project button
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/a[2]')))
            create_project_button = driver.find_element_by_xpath('/html/body/div/a[2]')
            create_project_button.click()

            # Create new project
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/form')))
            name_text = driver.find_element_by_xpath('//*[@id="Name"]')
            name_text.send_keys(new_client_project)
            create_button = driver.find_element_by_xpath('/html/body/div/div[1]/div/form/div[2]/input')
            create_button.click()

            # Assert project table
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/table/tbody')))
            client_projects_table = driver.find_element_by_xpath('/html/body/div/table/tbody')
            client_projects_table_rows = client_projects_table.find_elements_by_xpath('tr')

            # Search on table the name of the project
            project_exists = False
            for x in client_projects_table_rows:
                project_name = x.find_element_by_xpath('td[1]')
                if(project_name.text == new_client_project):
                    actionChains = ActionChains(driver)
                    actionChains.double_click(project_name).perform()
                    project_exists = True
                    break
            
            # Assert project created
            assert project_exists == True
            driver.get_screenshot_as_file(screeenshots_directory + "create_project.png")

        except AssertionError:
            driver.get_screenshot_as_file(screeenshots_directory + "create_project_error.png")
            print("Project creation failed!")
            raise
        except TimeoutException:
            driver.get_screenshot_as_file(screeenshots_directory + "create_project_error.png")
            print("Project creation failed!")
            raise
        except:
            driver.get_screenshot_as_file(screeenshots_directory + "create_project_error.png")
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # Client creation test case
    def test_create_client(self):
        try:
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

            # Assert clients table
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/table/tbody')))
            clients_table = driver.find_element_by_xpath('/html/body/div/table/tbody')
            clients_table_rows = clients_table.find_elements_by_xpath('tr')

            # Search on table the name of the client
            client_exists = False
            for x in clients_table_rows:
                client_name = x.find_element_by_xpath('td[1]')
                if(client_name.text == new_client_name):
                    actionChains = ActionChains(driver)
                    actionChains.double_click(client_name).perform()
                    client_exists = True
                    break
            
            # Assert client created
            assert client_exists == True
            driver.get_screenshot_as_file(screeenshots_directory + "create_client.png")

        except AssertionError:
            driver.get_screenshot_as_file(screeenshots_directory + "create_client_error.png")
            print("Client creation failed!")
            raise
        except TimeoutException:
            driver.get_screenshot_as_file(screeenshots_directory + "create_client_error.png")
            print("Client creation failed!")
            raise
        except:
            driver.get_screenshot_as_file(screeenshots_directory + "create_client_error.png")
            print("Unexpected error:", sys.exc_info()[0])
            raise

    # End process function
    def tearDown(self):
        self.driver.close()
        self.driver.quit()

if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output=reports_directory))