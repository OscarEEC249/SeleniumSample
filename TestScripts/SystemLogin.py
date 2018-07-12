import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_name = sys.argv[1]
user_password = sys.argv[2]

try:
    # Create WebDriver
    driver = webdriver.Chrome("C:\\SeleniumWebDrivers\\chromedriver.exe")
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
        print("Username assert failed!")
        print("Found value is: " + user_name.text)

    driver.close()
    driver.quit()
except NameError as error:
    print("Unexpected error:: {0}".format(error))
    driver.close()
    driver.quit()