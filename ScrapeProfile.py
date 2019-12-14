import bs4
import ParseInfo as Pi
import conf
import json
import FindImageUrls
import Api


with open(conf.JSON) as json_file:
    dict_data = json.load(json_file)

def scrape_profile(driver, profile_id, num_pics):
    """ Scraping the desired content from the profile page
    and returning the selenium driver and the and the profile's data.
    the data is organized as a dict with the following keys (if there is no data it will be None):
    Name, Age, Location, Sexual Orientation, Gender, Status, Relationship Type, Height, Body type,Ethnicity, Speaks,
    Politics, Education, Religion, Tobacco, Drinks, Drugs, Marijuana, Kids, Pets, Sign, Diet

            Parameters
            ----------
            driver : selenium webdriver object
                a webdriver on the profile page of a user

            profile_id : str
                the unique profile id (given by the enter_profile function)

            num_pics : int
                the number of pictures the user uploaded of himself (given by the enter_profile function)

            Returns
            -------
            driver : selenium webdrivre object
                a driver on on the home page

            data : dictionary
                dictionary with all of the scraped data from the profile.
    """

    # getting and parsing the content of the profile page
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    # finding the urls of the pictures of the users
    images_url = FindImageUrls.find_image_url(soup)
    # sending the pictures to the api for it to predict based on
    img_profile = images_url[0]
    img_compare = tuple(images_url[1:])
    preds = Api.api(img_profile, img_compare)
    # finding and getting the data from the page
    age = soup.find(class_="profile-basics-asl-age").get_text()
    location = soup.find(class_="profile-basics-asl-location").get_text().lower()

    # taking all the details
    data = {'profile_id': profile_id, 'age': age, 'location': location, 'num_pics': num_pics}
    details_temp = [detail.get_text().lower() for detail in soup.find_all(class_="matchprofile-details-text")]
    data = Pi.parse_info(data, details_temp, dict_data)
    data.update(preds)
    driver.find_elements_by_id("pass-button")[1].send_keys('\n')
    driver.get(conf.HOME_URL)

    return driver, data
