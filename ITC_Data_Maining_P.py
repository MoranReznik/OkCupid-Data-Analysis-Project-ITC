import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SITE_URL = "https://www.okcupid.com"
LOGIN_URL = "https://www.okcupid.com/login"
CHROME_DRIVER_PATH = "chromedriver.exe"
HOME_URL = "https://www.okcupid.com/home"
PAGES = 10


def site_login():
    """ login into OkCupid site and return the selenium driver in the home page """
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.get(LOGIN_URL)
    driver.find_element_by_name("username").send_keys("itc.proje@gmail.com")
    driver.find_element_by_name("password").send_keys("itc_pass4")
    driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    url = driver.current_url
    while url == LOGIN_URL:
        time.sleep(1)
        url = driver.current_url
    return driver


def enter_profile(driver):
    """ Move from the homepage to the profile page and return the selenium driver """
    home_page_content = driver.page_source
    soup = BeautifulSoup(home_page_content, 'html.parser')
    profile_url = SITE_URL + soup.find(class_="cardsummary-item cardsummary-profile-link").find('a', href=True)['href']
    driver.get(profile_url)
    return driver


def wait_for_profile_to_load(driver):
    """ wait for all relevant classes and ids to be loaded before we try t scrape the page """
    # We need to add all the classes and IDs to the lists ############################################################
    class_list = ["profile-basics-username", "profile-basics-asl-age", "profile-basics-asl-location",
                  "matchprofile-details-text"]
    id_list = ["pass-button"]
    max_wait_time = 100
    for class_name in class_list:
        WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    for id_name in id_list:
        WebDriverWait(driver, max_wait_time).until(EC.presence_of_element_located((By.ID, id_name)))
    return driver


def scrape_profile(driver):
    """ Scraping the desired content from the profile page
    and returning the selenium driver and the and the profile's data.
    the data is organized as a dict with the following keys (if there is no data it will be None):
    Name, Age, Location, Sexual Orientation, Gender, Status, Relationship Type, Height, Body type,Ethnicity, Speaks,
    Politics, Education, Religion, Tobacco, Drinks, Drugs, Marijuana, Kids, Pets, Sign, Diet """
    details = []
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    name = soup.find(class_="profile-basics-username").get_text()
    print(name)  # we will remove this later on  ##############################################################
    age = soup.find(class_="profile-basics-asl-age").get_text()
    location = soup.find(class_="profile-basics-asl-location").get_text()
    details_unorganized = [detail.get_text() for detail in soup.find_all(class_="matchprofile-details-text")]

    data = {'Name': name, 'Age': age, 'Location': location}

    # here there is a bunch of code that should be re-written, the goal is to
    # add all of the details of the women to the dict
    for detail in details_unorganized:
        details += detail.split(',')
    for detail in details:
        detail = detail.strip(' ')
        kind = find_kind_of_detail(detail)
        if not kind:
            data[kind] = detail

    driver.find_elements_by_id("pass-button")[1].send_keys('\n')
    driver.get(HOME_URL)
    return driver, data


def find_kind_of_detail(string):
    """helper func for the scrape func. in order to place a single detail on a person
    in the right key, we need to know to what category this detail belongs to
    possible categories are specified in the scrape func's docstring"""

    sequel_orientation = [['Straight', 'Gay', 'Bisexual', 'Asexual',
                          'Demisexual', 'Lesbian', 'Pansexual'], 'Sexuel Oriantaion']
    gender = [['Man', 'Woman', 'Agender', 'Androgynous', 'Bigender', 'Cis Man', 'Cis Woman', 'Genderfluid'], 'Gender']
    status = [['Single', 'Seeing Someone', 'Married'], 'Status']
    relationship_type = [['Monogamous', 'Non-monogamous'], 'Relationship Type']
    height = [["3'", "4'", "5'", "6'", "7'"], 'Height']
    body_type = [['Thin', 'Overweight', 'Average Build', 'Fit', 'Jacked', 'A little extra', 'Curvy', 'Full figured'],
                 'Body Type']
    ethnicity = [['Asian', 'Black', 'Hispanic/Latin', 'Indian', 'Middle Eastren', 'Native American',
                  'Pacific Islander', 'White'], 'Ethnicity']
    speaks = [['Speaks Hebrew', 'Speaks English', 'Speaks French', 'Speaks Russian', 'Speaks Arabic'], 'Speaks']
    politics = [['Politically liberal', 'Politically moderate', 'Politically conservative'], 'Politics']
    education = [['High school', 'Two-year college', 'University', 'Post-grad'], 'Education']
    religion = [['Agnosticism', 'Atheism', 'Christianity', 'Judaism', 'Catholicism', 'Islam', 'Hinduism', 'Buddhism'],
                'Religion']
    tobacco = [['Often', 'Sometimes', "Doesn't smoke cigarettes"], 'Tobacco']
    drinks = [['Often', 'Sometimes', 'Never'], 'Drinks']
    drugs = [['Often', 'Sometimes', 'Never'], 'Drugs']
    marijuana = [['Often', 'Sometimes', 'Never'], 'Marijuana']
    kids = [['Has Kid(s)', "Doesn't have kids"], 'Kids']
    pets = [['Has Dogs', 'Has cats'], 'Pets']
    sign = [['Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'leo',
             'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn'], 'Sign']
    diet = [['Omnivore', 'Vegeterain', 'Vegan', 'Kosher', 'Halal'], 'Diet']

    categories = [sequel_orientation, gender, status, relationship_type, height, body_type, ethnicity, politics,
                   education, religion, tobacco, drinks, drugs, marijuana, kids, pets, sign, diet]

    for category in categories:
        if string in category[0]:
            return category[1]


def main():
    all_data = {}
    driver = site_login()
    for i in range(PAGES):
        print("Page number %s" % str(i+1))
        profile_driver_unloaded = enter_profile(driver)
        profile_driver_loaded = wait_for_profile_to_load(profile_driver_unloaded)
        driver, all_data[i+1] = scrape_profile(profile_driver_loaded)

    print(all_data)


if __name__ == '__main__':
    main()
