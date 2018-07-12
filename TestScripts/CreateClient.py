import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_name = sys.argv[1]
user_password = sys.argv[2]
new_client_name = sys.argv[3]

def SystemLogin(user_name,user_password):
    try:
        # Create WebDriver
        driver = webdriver.Chrome("E:\\SeleniumWebDrivers\\Windows\\chromedriver.exe")
        # driver.manage().timeouts().pageLoadTimeout(100, SECONDS)
        driver.set_page_load_timeout(120)

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

        # Get username logged
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div[2]/ul[2]/li[1]")))
        user_name_label = driver.find_element_by_xpath('/html/body/nav/div/div[2]/ul[2]/li[1]')

        # Assert of username logged
        try: 
            assert user_name_label.text == 'Hello ' + user_name + '!'
        except AssertionError as error:
            print("Username assert failed!", 'red')
            print("Found value is: " + user_name.text, 'red')
        
        return driver
    except NameError as error:
        print("Unexpected error:: {0}".format(error))
        driver.close()
        driver.quit()

########################################### MAIN ###########################################

try:
    # Login to system
    driver = SystemLogin(user_name, user_password)
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

    # Search created client
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/table/tbody')))
    clients_table = driver.find_element_by_xpath('/html/body/div/table/tbody')
    clients_table_rows = clients_table.find_elements_by_xpath('tr')

    # Search on table the name of the client
    client_exists = False
    for x in clients_table_rows:
        client_name = x.find_element_by_xpath('td[1]')
        if(client_name.text == new_client_name):
            client_exists = True
            break
    
    # Assert client exists
    try: 
        assert client_exists == True
    except AssertionError as error:
        print("User was not created!")
    
    driver.close()
    driver.quit()
except:
    print("Unexpected error:", sys.exc_info())
    driver.close()
    driver.quit()