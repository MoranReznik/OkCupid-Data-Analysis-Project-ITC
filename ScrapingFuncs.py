# imports
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import DictData

# defining constants
SITE_URL = "https://www.okcupid.com"
LOGIN_URL = "https://www.okcupid.com/login"
CHROME_DRIVER_PATH = "chromedriver.exe"
HOME_URL = "https://www.okcupid.com/home"


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


def enter_profile(driver):
    """ Move from the homepage to the profile page and return the selenium driver. also get number of
    photos the person uploded of himself"""

    # getting and parsing the content of the doubletake page
    num_pics = len(driver.find_elements_by_css_selector('[alt="A photo"]')) - 10  # there are always 10 photos in this
    # page that are not of the person presented in this page
    home_page_content = driver.page_source
    soup = BeautifulSoup(home_page_content, 'html.parser')
    # finding the url if the profile page and entering it
    profile_url = SITE_URL + soup.find(class_="cardsummary-item cardsummary-profile-link").find('a', href=True)['href']
    driver.get(profile_url)

    return driver, num_pics


def wait_for_profile_to_load(driver):
    """ wait for all relevant classes and ids to be loaded before we try t scrape the page """

    class_list = ["profile-basics-username", "profile-basics-asl-age", "profile-basics-asl-location",
                  "matchprofile-details-text"]
    id_list = ["pass-button"]
    max_wait_time = 20
    for class_name in class_list:
        WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located((By.CLASS_NAME, class_name)))
    for id_name in id_list:
        WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located((By.ID, id_name)))
    return driver


def scrape_profile(driver, num_pics):
    """ Scraping the desired content from the profile page
    and returning the selenium driver and the and the profile's data.
    the data is organized as a dict with the following keys (if there is no data it will be None):
    Name, Age, Location, Sexual Orientation, Gender, Status, Relationship Type, Height, Body type,Ethnicity, Speaks,
    Politics, Education, Religion, Tobacco, Drinks, Drugs, Marijuana, Kids, Pets, Sign, Diet """

    details = []

    # getting and parsing the content of the profile page
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    # finding and getting the data from the page
    name = soup.find(class_="profile-basics-username").get_text()
    age = soup.find(class_="profile-basics-asl-age").get_text()
    location = soup.find(class_="profile-basics-asl-location").get_text()
    data = {'Name': name, 'Age': age, 'Location': location}
    details_temp = [detail.get_text() for detail in soup.find_all(class_="matchprofile-details-text")]
    # splitting data that is separated by a comma
    for detail in details_temp:
        details += detail.split(',')
    # removing whitespaces
    for detail in details:
        kind = find_kind_of_detail(detail.strip())
        # handling several kinds of details that are formatted in a special way
        if kind == 'speaks':
            detail = detail[7:]  # remove the word speaks from the string
            languages = detail.replace('and', ',')
            languages = languages.replace(', some', ',')
            languages = languages.split(',')
            for index, language in enumerate(languages):
                languages[index] = language.strip(' ')
            data[kind] = languages

        elif kind == 'Religion':
            detail = detail.split(' (')
            if len(detail) > 1:
                data['Religion'] = detail[0]
                data['Religion importance'] = detail[1][:-1]
            else:
                data['Religion'] = detail[0]
        elif kind == 'Height':
            detail = detail[:-2]
            data[kind] = detail
        elif kind == 'Looking for gender':
            detail = detail[12:]
            detail = detail.replace("short-term", 'short')
            detail = detail.replace("long-term", 'short')
            detail = detail.replace("and new", '')
            detail = detail.replace(".", '')
            detail = detail.split(' ')
            connection = [i for i in detail if i in ["short", "long", "hookups", "friends"]]
            gender = [i for i in detail if
                      i in ['men', 'women', 'agenders', 'androgynes', 'bigenders', 'cis Men', 'cis Women',
                            'genderfluids', 'genderqueers', 'genders nonconforming', 'hijras', 'intersexes',
                            'non-binaries', 'others', 'pangenders', 'transfeminines', 'transgenders',
                            'transmasculines', 'transsexuals', 'trans Men', 'trans Women', 'two Spirits']]
            data["Looking for gender"] = gender
            data["Looking for connection"] = connection

        elif kind:
            data[kind] = detail.strip()
    data['num_pics'] = num_pics
    print(data)
    driver.find_elements_by_id("pass-button")[1].send_keys('\n')
    driver.get(HOME_URL)
    return driver, data


def find_kind_of_detail(string):
    """helper func for the scrape func. in order to place a single detail on a person
    in the right key, we need to know to what category this detail belongs to
    possible categories are specified in the scrape func's docstring"""

    for key, values in DictData.choices.items():
        for value in values:
            if value.lower() in string.lower():
                return key
