import selenium.webdriver.support.ui as sel_ui
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def wait_for_profile_to_load(driver):
    """ wait for all relevant classes and ids to be loaded before we try to scrape the page

                Parameters
                ----------
                driver : a selenium webdriver object
                    a web driver in the profile page of a user


                Returns
                -------
                driver : selenium webdriver object
                    the input driver, after finishing loading all of the classes
        """

    class_list = ["profile-basics-username", "profile-basics-asl-age", "profile-basics-asl-location",
                  "matchprofile-details-text"]
    id_list = ["pass-button"]
    max_wait_time = 20
    for class_name in class_list:
        sel_ui.WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located((By.CLASS_NAME, class_name)))
    for id_name in id_list:
        sel_ui.WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located((By.ID, id_name)))
    return driver
