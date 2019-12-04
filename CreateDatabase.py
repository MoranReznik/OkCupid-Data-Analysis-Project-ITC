# pip install mysql-connector-python
import mysql.connector
import json
import GV
import argparse

""" creating MySQL database and tables, if they don't exist.
The profiles table contains an incremented main_id as the PK, the unique user_id (which we encrypt) and
scraper profile name, in addition to the age, height, location and pics_num for each okcupid profile we scraped.
Other categories which have a finite number of options have their own table with the main_id as the foreign key.
"""

# creating the flags
parser = argparse.ArgumentParser(description='username and password for the creation of mySQL server')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', nargs=str, help='password')
args = parser.parse_args()

with open('choices.json') as json_file:
    columns = list(json.load(json_file).keys())

columns.remove('Height')
columns += ['Religion_importance']

con = mysql.connector.connect(
    host='localhost', user=args.username, passwd=args.password, auth_plugin='mysql_native_password')
cur = con.cursor()

cur.execute(''' CREATE DATABASE IF NOT EXISTS okcupid_project ''')
cur.execute(''' USE okcupid_project ''')

sql = ''' CREATE TABLE IF NOT EXISTS profiles
(main_id INT NOT NULL AUTO_INCREMENT, Profile_id VARBINARY(255) NOT NULL UNIQUE, Age INT DEFAULT NULL, 
Height INT DEFAULT NULL, Location VARCHAR(255) DEFAULT NULL, Num_pics INT DEFAULT NULL, PRIMARY KEY (main_id)) '''

cur.execute(sql)

for column in columns:
    insert = (column, column)
    sql = ''' CREATE TABLE IF NOT EXISTS %s (id INT NOT NULL AUTO_INCREMENT, main_id INT NOT NULL, 
    %s VARCHAR(255) DEFAULT NULL, PRIMARY KEY (id), FOREIGN KEY(main_id) REFERENCES profiles(main_id)) ''' % insert
    cur.execute(sql)

con.commit()
con.close()



