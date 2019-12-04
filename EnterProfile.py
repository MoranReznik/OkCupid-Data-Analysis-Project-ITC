import bs4
import conf


def enter_profile(driver):
    """ Move from the homepage to the profile page and return the selenium driver. also get number of
    photos the person uploaded of himself

            Parameters
            ----------
            driver : selenium webdriver object
                gets a webdriver in a doubletake page of a person


            Returns
            -------
            driver : selenium webdriver object
                the input driver, now inside the profile of the person

            num_pics : int
                the number of pictures the user uploaded of himself.

            profile_id : str
                the unique profile id

    """

    # getting and parsing the content of the doubletake page
    num_pics = len(driver.find_elements_by_css_selector('[alt="A photo"]')) - 10  # there are always 10 photos in this
    # page that are not of the person presented in this page
    home_page_content = driver.page_source
    soup = bs4.BeautifulSoup(home_page_content, 'html.parser')
    # finding the url if the profile page and entering it
    address = soup.find(class_="cardsummary-item cardsummary-profile-link").find('a', href=True)['href']
    profile_id = address.split('/')[-1].split('?')[0]
    profile_url = conf.SITE_URL + address
    driver.get(profile_url)

    return driver, num_pics, profile_id
