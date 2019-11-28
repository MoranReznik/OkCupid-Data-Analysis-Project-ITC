# GV stands for GlobalVariables

# EnterProfiles.py
SITE_URL = "https://www.okcupid.com"

# Main.py
PROFILES = {"straight_female": {"user": "itc.proje@gmail.com", "pass": "itc_pass4", "data": {}},
            "straight_male": {"user": "shirella111@gmail.com", "pass": "itcpass123", "data": {}}}

# ScrapeProfile.py
HOME_URL = "https://www.okcupid.com/home"

# SiteLogin.py
CHROME_DRIVER_PATH = "chromedriver.exe"
LOGIN_URL = "https://www.okcupid.com/login"

# CLIArguments
profiles_help = 'what kind of profiles to scrape. options are:' \
                'straight_female, straight_male. if this flag is not set, take all possible kind of profiles.' \
                'this argument also controls the order of scraping '

information_help = 'what information to scrape from each profile, if available. if this flag is not set,' \
                   ' take all possible information. ' \
                   ' the options are:' \
                   'Name, Age, Location, Sexual_Orientation,Gender,Status,Relationship_Type,Height,Body_Type,' \
                   'Ethnicity, speaks, Politics, Education, Religion, Tobacco, Drinks, Drugs, Marijuana, Kids,' \
                   'Pets, Sign, Diet, Looking_for_gender, Looking_for_connection, number_of_pics'

required_details = ['Name', 'Age', 'Location', 'Sexual_Orientation', 'Gender', 'Status', 'Relationship_Type',
                    'Height', 'Body_Type', 'Ethnicity', 'speaks', 'Politics', 'Education', 'Religion',
                    'Tobacco', 'Drinks', 'Drugs', 'Marijuana', 'Kids', 'Pets', 'Sign', 'Diet',
                    'Looking_for_gender', 'Looking_for_connection', 'number_of_pics']
