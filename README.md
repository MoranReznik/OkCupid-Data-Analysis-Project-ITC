# HELLO THERE and welcome to our OkCupid WebScraper!

#### this guide's goal is to help you understand how to operate the scraper. 
#### Our scraper is designed in order to scrape data on profiles from the OkCupid website. 

the scraper is used through the command line. before using it, you should create a mySQL database to hold the data (unless you only want it printed to stdout).
in order to do this, run the following command:

python CreateDatabase.py username password

where username and password is your mySQL server credentials.

then, you will be able to run the webscraper, with the following syntax:

python Main.py mode required_args optional_args
 
the scraper has 3 modes:

### PRINT :
the simplest mode, will scrape profiles data and print it for you. 
it has 1 required arg:

		1.-n number_of_profiels_to_scrape_for_each_profile_type 
		
(there are two profie types: man and women)
		
### WRITE:
write the data scraped into the database. 
it has 2 required args:
  
		1.-c mySQL_server_username mySQL_server_password

		2.-n number_of_profiels_to_scrape_for_each_profile_type 
		
(there are two profie types: man and women)

### READ:
query the database.
it has 1 reqired arg:

		1.-c mySQL_server_username mySQL_server_password

it has a lot of optional args.  you can see them all using the help flag in the CLI, but here is an example of use:

	python Main.py read --age 20 30 --gender man -information location drugs
	
this will show you only profiles of man in age 20 to 30, the data it will show on this profiles is their location and use of drugs. 
the --information flags selects the kind of data you will see about the profiles. the other optional flags works like a 'where' clause in sql. 
#### you can also write the result of the query into a csv file! just use the flag --write_csv name_of_file in read mode!

# *** the API ***
the scraper is enriched by a n external api, that takes the pictures of a profile and return some predictions on it: the age of the person, the face expression of the person, a similar celeb to that person and is all of the photos belongs to the same person.

# ***PROTECTING THE PRIVECY OF THE USERS***:
there is no last name in the database - only first name. the only unique identifier - their OkCupid profile id, is encryped.
