
# coding: utf-8

# In[8]:

# imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import warnings
warnings.filterwarnings('ignore')


LOGIN_URL = "https://www.okcupid.com/login" # url for the login page in okcupid


def site_login(login_url):
    """goal: loging in to the OkCupid Site using fake account details 
       input: url of the login page of the site
       output: returns the driver at the first doubletake page"""

    # getting the content of the login page
    driver = webdriver.Chrome(executable_path="chromedriver.exe") # opening the browser
    driver.get(login_url) # going to the login page
    # logging in by finding the ID and password bars and filling them 
    driver.find_element_by_name("username").send_keys("itc.proje@gmail.com")
    driver.find_element_by_name("password").send_keys("itc_pass4")
    # pressing the "login" button
    driver.find_element_by_class_name("login2017-actions-button").send_keys('\n')
    # getting the url of the first doubletake page to which we arrive after login
    url = driver.current_url
    # making sure the page was loaded. if not, wait more time. 
    while url == login_url:
        url = driver.current_url

    return driver

def doubletake_to_profile(driver):
    """goes from a doubletake page to the profile, where there is more data
    input: driver at the doubletake page
    output: driver at the profile page"""
    
    driver.find_element_by_link_text("View Profile").click() # clicking on the "view profile" button

    # making sure the page is loded with all desirable data b4 moving on
    time_to_wait = 50
    wait = WebDriverWait(driver,time_to_wait)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"profile-basics-username")))
    
    wait = WebDriverWait(driver,time_to_wait)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"profile-basics-asl-age")))
    
    wait = WebDriverWait(driver,time_to_wait)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"profile-basics-asl-location")))
    
    wait = WebDriverWait(driver,time_to_wait)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"matchprofile-details-text")))
    
    return driver

def scrape(driver):
    """getting the desired content from a single profile on OkCupid
    input: the driver in a profile page
    output: the data about the person who owns the profile, and driver in the profile page
    the data is orgenized as a dict with the following keys (if there is no data it will be None):
    Name, Age, Location, Sexuel Oriantaion, Gender, Status, Relationship Type, Height, Body type,Ethnicity, Speaks,
    Politics, Education, Religion, Tobacco, Drinks, Drugs, Marijuana, Kids, Pets, Sign, Diet
    """
    
    # parsing the content of the page
    content = driver.page_source
    soup = BeautifulSoup(content)

    # finding the data in the prased page

    name = soup.find(class_="profile-basics-username").get_text()
    age = soup.find(class_="profile-basics-asl-age").get_text()
    location = soup.find(class_="profile-basics-asl-location").get_text()
    dets = [p.get_text() for p in soup.find_all(class_="matchprofile-details-text")]

    data = {}
    data['Name'] = name
    data['Age'] = age
    data['Location'] = location
    details = []
    
    # here there is a bunch of code that sould be re-written, the goal is to
    # add all of the details of the women to the dict
    for i in dets:
        details += i.split(',')
    for detail in details:
        detail = detail.strip(' ')
        kind = find_kind_of_detail(detail)
        if kind is not None:
            data[kind] = detail

    return data, driver

def find_kind_of_detail(string):
    """helper func for the scrape func. in order to place a single detali on a person
    in the right key, we need to know to what category this detali belongs to
    possible categories are specified in the scrape func's docstring"""
    
    sexuel_oriantaion = [['Straight','Gay','Bisexual','Asexual',
                               'Demisexual','Lesbian','Pansexual'],'Sexuel Oriantaion']
    gender = [['Man','Woman','Agender','Androgynous','Bigender','Cis Man','Cis Woman','Genderfluid'],'Gender']
    status = [['Single','Seeing Someone','Married'],'Status']
    relationship_type = [['Monogamous','Non-monogamous'],'Relationship Type']
    height = [["3'","4'","5'","6'","7'"],'Height']
    body_type = [['Thin','Overweight','Average Build','Fit','Jacked','A little extra','Curvy','Full figured'],'Body Type']
    ethnicity = [['Asian','Black','Hispanic/Latin','Indian','Middle Eastren','Native American',
                  'Pacific Islander','White'],'Ethnicity']
    speaks = [['Speaks Hebrew','Speaks English','Speaks French','Speaks Russian','Speaks Arabic'],'Speaks']
    politics = [['Politically liberal','Politically moderate','Politically conservative'],'Politics']
    education = [['High school','Two-year college','University','Post-grad'],'Education']
    religion = [['Agnosticism','Atheism','Christianity','Judaism','Catholicism','Islam','Hinduism','Buddhism'],'Religion']
    tobacco = [['Often','Sometimes',"Doesn't smoke cigarettes"],'Tobacco']
    drinks = [['Often','Sometimes','Never'],'Drinks']
    drugs = [['Often','Sometimes','Never'],'Drugs']
    marijuana = [['Often','Sometimes','Never'],'Marijuana']
    kids = [['Has Kid(s)',"Doesn't have kids"],'Kids']
    pets = [['Has Dogs','Has cats'],'Pets']
    sign = [['Aquarius','Pisces','Aries','Taurus','Gemini','Cancer','leo',
             'Virgo','Libra','Scorpio','Sagittarius','Capricorn'],'Sign']
    diet = [['Omnivore','Vegeterain','Vegan','Kosher','Halal'],'Diet']
    
    catergories = [sexuel_oriantaion,gender,status,relationship_type,height,body_type,ethnicity,politics,education,
                   religion,tobacco,drinks,drugs,marijuana,kids,pets,sign,diet]
    
    for catergory in catergories:
        if string in catergory[0]:
            return catergory[1]

def profile_to_doubletake(driver):
    """input: driver at a profile page
    output: driver at the same person's doubletake page"""
    
    driver.back()
    
    return driver
        
def change_person(driver):
    """input: driver at a doubletake page
    presses the dislike button in order to get a new person's detalis
    ouput: driver on a new person's doubletake page"""  
    
    driver.find_element_by_class_name("pass-pill-button-inner").click()
    
    return driver
    
def main():
    driver = site_login(LOGIN_URL)
    
    for i in range(10):
        driver = doubletake_to_profile(driver)
        detalis, driver = scrape(driver)
        driver = profile_to_doubletake(driver)
        driver = change_person(driver)
        print(i)
    
    
    
if __name__ == '__main__':
    main()

