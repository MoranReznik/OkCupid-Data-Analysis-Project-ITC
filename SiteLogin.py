from selenium import webdriver
import time

CHROME_DRIVER_PATH = "chromedriver.exe"
LOGIN_URL = "https://www.okcupid.com/login"

def site_login(login_details):
    """ login into OkCupid site and return the selenium driver in the home page """

    # setting up the driver and entering the login page
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.get(LOGIN_URL)

    # enter the login details
    driver.find_element_by_name("username").send_keys(login_details["user"])
    driver.find_element_by_name("password").send_keys(login_details["pass"])
    driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    url = driver.current_url

    # making sure page is loaded and returning the driver
    while url == LOGIN_URL:
        time.sleep(1)
        url = driver.current_url
    return driver