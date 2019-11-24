from bs4 import BeautifulSoup

SITE_URL = "https://www.okcupid.com"

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