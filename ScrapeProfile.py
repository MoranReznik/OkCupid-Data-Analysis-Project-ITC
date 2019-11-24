from bs4 import BeautifulSoup
from FindKindOfDetail import find_kind_of_detail

HOME_URL = "https://www.okcupid.com/home"

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