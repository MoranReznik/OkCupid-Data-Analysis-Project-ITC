from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import GV


def site_login(login_details):
    """ login into OkCupid site and return the selenium driver in the home page

                Parameters
                ----------
                login_details : dictionary
                    a dictionary holding the user id and password for a single user.


                Returns
                -------
                driver : selenium webdrivre object
                    a driver on on the home page
        """

    # setting up the driver and entering the login page
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=GV.CHROME_DRIVER_PATH, options=chrome_options)
    driver.get(GV.LOGIN_URL)

    # enter the login details
    driver.find_element_by_name("username").send_keys(login_details["user"])
    driver.find_element_by_name("password").send_keys(login_details["pass"])
    driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    url = driver.current_url

    # making sure page is loaded and returning the driver
    while url == GV.LOGIN_URL:
        time.sleep(1)
        url = driver.current_url
    return driver
