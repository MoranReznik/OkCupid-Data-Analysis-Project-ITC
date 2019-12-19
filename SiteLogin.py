from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import selenium.common
import time
import conf
import platform


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
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    operating_system = platform.system()
    driver = webdriver.Chrome(executable_path=conf.CHROME_DRIVER_PATH[operating_system], options=chrome_options)
    driver.get(conf.LOGIN_URL)

    # enter the login details
    # 19/12/19: There are now two different login pages which seem to be chosen randomly..
    try:
        driver.find_element_by_name("username").send_keys(login_details["user"])
        driver.find_element_by_name("password").send_keys(login_details["pass"])
        driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    except selenium.common.exceptions.ElementNotInteractableException:
        driver.find_elements_by_class_name("login-fields-field")[0].find_element_by_name("username").\
            send_keys(login_details["user"])
        driver.find_elements_by_class_name("login-fields-field")[1].find_element_by_name("password").\
            send_keys(login_details["pass"])
        driver.find_element_by_class_name("login-actions-button").send_keys('\n')
    url = driver.current_url

    # making sure page is loaded and returning the driver
    while url == conf.LOGIN_URL:
        time.sleep(1)
        url = driver.current_url
    return driver
