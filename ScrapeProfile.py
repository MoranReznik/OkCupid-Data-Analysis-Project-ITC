import bs4
import FindKindOfDetail
import ParseInfo as Pi
import GV


def scrape_profile(driver, profile_id, num_pics, mode):
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

            required_details : list
                a list of the kind of details the user wants to collect about the OkCupid profiles.

            Returns
            -------
            driver : selenium webdrivre object
                a driver on on the home page

            data : dictionary
                dictionary with all of the scraped data from the profile.
    """

    details = []

    # getting and parsing the content of the profile page
    content = driver.page_source
    soup = bs4.BeautifulSoup(content, 'html.parser')
    # finding and getting the data from the page
    age = soup.find(class_="profile-basics-asl-age").get_text()
    location = soup.find(class_="profile-basics-asl-location").get_text()

    # taking all the details
    data = {'profile_id': profile_id, 'age': age, 'location': location, 'num_pics': num_pics}

    details_temp = [detail.get_text() for detail in soup.find_all(class_="matchprofile-details-text")]
    # splitting data that is separated by a comma
    for detail in details_temp:
        details += detail.split(',')
    # removing whitespaces
    for detail in details:
        # find category of detail
        kind = FindKindOfDetail.find_kind_of_detail(detail.strip())
        # parse detail
        detail = Pi.parse_info(detail, kind)
        # handling several kinds of details that are formatted in a special way
        if kind == 'religion':
            if len(detail) > 1:
                data['religion'] = detail[0]
                data['religion_importance'] = detail[1]
            else:
                data['religion'] = detail[0]

        elif kind == 'looking_for_gender':
            data["looking_for_gender"] = detail[0]
            data["looking_for_connection"] = detail[1]

        elif kind == 'speaks' and 'speaks' in data:
            data[kind] += detail

        else:
            data[kind] = detail
    if 'relationship_Type' in data:
        print('\n\n')
        rt = data['relationship_Type']

        for gen in ['man','women','people']:
            if gen in rt:
                data["looking_for_gender"] = gen
                if 'non' in rt:
                    data['Relationship_Type'] = 'non-monogamous'
                else:
                    data['Relationship_Type'] = 'monogamous'
        for con in ["short", "long", "hookups", "friends"]:
            if con in rt:
                data["Looking_for_connection"] = con
            if 'non' in rt:
                data['Relationship_Type'] = 'non-monogamous'
            else:
                data['Relationship_Type'] = 'monogamous'
    print(data)

    driver.find_elements_by_id("pass-button")[1].send_keys('\n')
    driver.get(GV.HOME_URL)
    return driver, data
