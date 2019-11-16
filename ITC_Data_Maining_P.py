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
    age = soup.find(class_="profile-basics-asl-age").get_text()
    location = soup.find(class_="profile-basics-asl-location").get_text()
    data = {'Name': name, 'Age': age, 'Location': location}

    details_temp = [detail.get_text() for detail in soup.find_all(class_="matchprofile-details-text")]
    for detail in details_temp:
        details += detail.split(',')

    for detail in details:
        kind = find_kind_of_detail(detail.strip())
        if kind:
            data[kind] = detail.strip()
    print(data)  # we will remove this later on  ##############################################################

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
        "Looking for status": ["single", "married"],
        "Looking for gender": ['Men', 'Women', 'Agenders', 'Androgynes', 'Bigenders', 'Cis Men', 'Cis Women',
                               'Genderfluids', 'Genderqueers', 'Genders Nonconforming', 'Hijras', 'Intersexes',
                               'Non-binaries', 'Others', 'Pangenders', 'Transfeminines', 'Transgenders',
                               'Transmasculines', 'Transsexuals', 'Trans Men', 'Trans Women', 'Two Spirits'],
        "Looking for connection": ["short", "long", "hookups", "new friends"]}

    for key, values in choices.items():
        for value in values:
            if value.lower() in string.lower():
                return key


def main():
    all_data = {}
    driver = site_login()
    for i in range(PAGES):
        print("Page number %s" % str(i + 1))
        profile_driver_unloaded = enter_profile(driver)
        profile_driver_loaded = wait_for_profile_to_load(profile_driver_unloaded)
        driver, all_data[i + 1] = scrape_profile(profile_driver_loaded)

    print(all_data)


if __name__ == '__main__':
    main()
