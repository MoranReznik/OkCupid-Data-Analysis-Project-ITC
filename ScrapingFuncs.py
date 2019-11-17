# imports
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# defining constants
SITE_URL = "https://www.okcupid.com"
LOGIN_URL = "https://www.okcupid.com/login"
CHROME_DRIVER_PATH = "chromedriver.exe"
HOME_URL = "https://www.okcupid.com/home"
PAGES = 30

def site_login(gender):
    """ login into OkCupid site and return the selenium driver in the home page """

    # setting up the driver and entering the login page
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver.get(LOGIN_URL)

    # for the requested gender, enter the login details and enter the site
    if gender == 'men':
        driver.find_element_by_name("username").send_keys("itc.proje@gmail.com")
        driver.find_element_by_name("password").send_keys("itc_pass4")
        driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    else:
        driver.find_element_by_name("username").send_keys("shirella111@gmail.com")
    driver.find_element_by_name("password").send_keys("itcpass123")
    driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    url = driver.current_url

    # making sure page is loaded and returning the driver
    while url == LOGIN_URL:
        time.sleep(1)
        url = driver.current_url
    return driver


def enter_profile(driver):
    """ Move from the homepage to the profile page and return the selenium driver """
    # getting and parsing the content of the doubletake page
    home_page_content = driver.page_source
    soup = BeautifulSoup(home_page_content, 'html.parser')
    # finding the url if the profile page and entering it
    profile_url = SITE_URL + soup.find(class_="cardsummary-item cardsummary-profile-link").find('a', href=True)['href']
    driver.get(profile_url)

    return driver


def wait_for_profile_to_load(driver):
    """ wait for all relevant classes and ids to be loaded before we try t scrape the page """

    class_list = ["profile-basics-username", "profile-basics-asl-age", "profile-basics-asl-location",
                  "matchprofile-details-text"]
    id_list = ["pass-button"]
    max_wait_time = 100
    for class_name in class_list:
        WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located((By.CLASS_NAME, class_name)))
    for id_name in id_list:
        WebDriverWait(driver, max_wait_time).until(ec.presence_of_element_located((By.ID, id_name)))
    return driver


def scrape_profile(driver):
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
    # splitting data that is seperated by a comma
    for detail in details_temp:
        details += detail.split(',')
    # removing whitespaces
    for detail in details:
        kind = find_kind_of_detail(detail.strip())
        # hendeling several kinds of details that are formatted in a special way
        if kind == 'speaks':
            detail = detail[7:]
            languages = detail.replace('and', ',')
            languages = languages.replace(', some', ',')
            languages = languages.split(',')
            for i, l in enumerate(languages):
                languages[i] = l.strip(' ')
            data[kind] = languages

        elif kind == 'Religion':
            detail = detail.split(' (')
            if len(detail) > 1:
                data['Religion'] = detail[0]
                data['Religion importence'] = detail[1][:-1]
            else:
                data['Religion'] = detail[0]

        elif kind == 'Looking for gender':
            detail = detail[12:]
            detail = detail.replace("short-term", 'short')
            detail = detail.replace("long-term", 'short')
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
    print(data)
    driver.find_elements_by_id("pass-button")[1].send_keys('\n')
    driver.get(HOME_URL)
    return driver, data


def find_kind_of_detail(string):
    """helper func for the scrape func. in order to place a single detail on a person
    in the right key, we need to know to what category this detail belongs to
    possible categories are specified in the scrape func's docstring"""

    choices = {
        'Sexual Orientation': ['Straight', 'Gay', 'Bisexual', 'Asexual', 'Demisexual', 'Lesbian', 'Pansexual', 'Queer',
                               'Questioning', 'Sapiosexual'],

        'Gender': ['Woman', 'Man', 'Agender', 'Androgynous', 'Bigender', 'Cis Man', 'Cis Woman', 'Genderfluid',
                   'Genderqueer', 'Gender Nonconforming', 'Hijra', 'Intersex', 'Non-binary', 'Other', 'Pangender',
                   'Transfeminine', 'Transgender', 'Transmasculine', 'Transsexual', 'Trans Man', 'Trans Woman',
                   'Two Spirit'],

        'Status': ['Single', 'Seeing Someone', 'Married'],

        'Relationship Type': ['Monogamous', 'Non-monogamous'],

        'Height': ["3'", "4'", "5'", "6'", "7'"],

        'Body Type': ['Thin', 'Overweight', 'Average Build', 'Fit', 'Jacked', 'A little extra', 'Curvy',
                      'Full figured'],

        'Ethnicity': ['Asian', 'Black', 'Hispanic / Latin', 'Indian', 'Middle Eastern', 'Native American',
                      'Pacific Islander', 'White', 'Other'],

        'speaks': ['English', 'Afrikaans', 'Albanian', 'Arabic', 'Armenian', 'Basque', 'Belarusian', 'Bengali',
                   'Breton', 'Bulgarian', 'Catalan', 'Cebuano', 'Chechen', 'Chinese', 'Chinese (Cantonese)',
                   'Chinese (Mandarin)', 'C++', 'Croatian', 'Czech', 'Danish', 'Dutch', 'Esperanto', 'Estonian',
                   'Finnish', 'French', 'Frisian', 'Georgian', 'German', 'Greek', 'Gujarati', 'Ancient Greek',
                   'Hawaiian', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Ilongo', 'Indonesian', 'Irish', 'Italian',
                   'Japanese', 'Khmer', 'Korean', 'Latin', 'Latvian', 'LISP', 'Lithuanian', 'Malay', 'Maori',
                   'Mongolian', 'Norwegian', 'Occitan', 'Other', 'Persian', 'Polish', 'Portuguese', 'Punjabi',
                   'Romanian', 'Rotuman', 'Russian', 'Sanskrit', 'Sardinian', 'Serbian', 'Sign Language', 'Slovak',
                   'Slovenian', 'Spanish', 'Swahili', 'Swedish', 'Tagalog', 'Tamil', 'Thai', 'Tibetan', 'Turkish',
                   'Ukrainian', 'Urdu', 'Vietnamese', 'Welsh', 'Yiddish'],

        'Politics': ['Politically liberal', 'Politically moderate', 'Politically conservative'],

        'Education': ['High school', 'Two-year college', 'University', 'Post-grad'],

        'Religion': ['Agnostic', 'Atheist', 'Christian', 'Jewish', 'Catholic', 'Islamic', 'Hindu',
                     'Buddhist', 'Sikh'],

        'Tobacco': ['Smokes cigarettes regularly', 'Smokes cigarettes sometimes', "Doesn't smoke cigarettes"],

        'Drinks': ['Drinks regularly', 'Drinks sometimes', 'Never drinks'],

        'Drugs': ['Does drugs regularly', 'Does drugs sometimes', "Doesn’t do drugs"],

        'Marijuana': ['Smokes marijuana regularly', 'Smokes marijuana sometimes', 'Never smokes marijuana'],

        'Kids': ['Has Kid(s)', "Doesn’t have kids", "Wants kids"],

        'Pets': ['Has dogs', 'Has cats'],

        'Sign': ['Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'leo', 'Virgo', 'Libra', 'Scorpio',
                 'Sagittarius', 'Capricorn'],

        'Diet': ['Omnivore', 'Vegetarian', 'Vegan', 'Kosher', 'Halal'],

        "Looking for gender": ['men', 'women', 'agenders', 'androgynes', 'bigenders', 'cis Men', 'cis Women',
                               'genderfluids', 'genderqueers', 'genders nonconforming', 'hijras', 'intersexes',
                               'non-binaries', 'others', 'pangenders', 'transfeminines', 'transgenders',
                               'transmasculines', 'transsexuals', 'trans Men', 'trans Women', 'two Spirits'],

        "Looking for connection": ["short", "long", "hookups", "new friends"]}

    for key, values in choices.items():
        for value in values:
            if value.lower() in string.lower():
                return key