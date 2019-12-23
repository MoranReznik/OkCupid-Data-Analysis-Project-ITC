# EnterProfiles.py
SITE_URL = "https://www.okcupid.com"

# Main.py
PROFILES = {"straight_male": {"user": "shirella111@gmail.com", "pass": "itcpass123", "data": {}},
            "straight_female": {"user": "itc.proje@gmail.com", "pass": "itc_pass4", "data": {}}}

# ScrapeProfile.py
HOME_URL = "https://www.okcupid.com/home"

# SiteLogin.py
CHROME_DRIVER_PATH = {'Windows': "chromedriver.exe", 'Linux': "/usr/bin/chromedriver"}
LOGIN_URL = "https://www.okcupid.com/login"

# CLIArguments
mode_help = '''mode to operate in. 
               read: reads from the database. required args: "my_sql_creds". opt args: kind of profiles,"information".
               write: scrape profiles and add them to database.  required args: "my_sql_creds"
               print: scrape profiles and send them to stdout'''

my_sql_creds_help = '''username and password for mySQL server. used in order to read or write to the database. 
should be formatted as "username password"'''

information_to_show_help = '''what information to scrape from each profile, if available. if this flag is not set,
                    take all possible information. ' \
                    the options are:' \
                   Name, Age, Location,Gender, Sexual_Orientation,Gender,Status,Relationship_Type,Height,Body_Type,
                   Ethnicity, speaks, Politics, Education, Religion, Tobacco, Drinks, Drugs, Marijuana, Kids,
                   Pets, Sign, Diet, Looking_for_gender, Looking_for_connection, number_of_pics'''

# json file with all the different ok_cupid option
JSON = 'choices.json'

# MYSQL database tables and columns
extra_tables = ['speaks', 'looking_for_connection', 'looking_for_gender']
profiles_columns = ['age', 'height', 'location', 'num_pics', 'sexual_orientation', 'gender', 'status',
                    'relationship_type', 'body_type', 'ethnicity', 'politics', 'education', 'religion',
                    'religion_importance', 'tobacco', 'drinks', 'drugs', 'marijuana', 'kids', 'pets', 'sign', 'diet',
                    'pred_gender', 'pred_age', 'pred_expression', 'pred_celeb', 'pred_pics_match']
