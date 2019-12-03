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

# CreateDatabase.py
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "KKkm73iaC2cnH3c#oMG$KD^JzA*f"
