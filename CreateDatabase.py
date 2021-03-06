# pip install mysql-connector-python
import mysql.connector
import argparse
import conf


""" creating MySQL database and tables, if they don't exist.
The profiles table contains an incremented main_id as the PK, the unique user_id (which we encrypt) and
scraper profile name, in addition to the age, height, location and pics_num for each okcupid profile we scraped.
Other categories which have a finite number of options have their own table with the main_id as the foreign key.
"""

# creating the flags
parser = argparse.ArgumentParser(description='username and password for the creation of mySQL database')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='password')
args = parser.parse_args()

con = mysql.connector.connect(
    host='localhost', user=args.username, passwd=args.password, auth_plugin='mysql_native_password')
cur = con.cursor()

cur.execute(''' CREATE DATABASE IF NOT EXISTS okcupid_project ''')
cur.execute(''' USE okcupid_project ''')

columns = ''
for col in conf.profiles_columns:
    var = 'VARCHAR(255)'
    if col in ['age', 'height', 'num_pics', 'pred_age']:
        var = 'INT'
    columns += ', %s %s DEFAULT NULL' % (col, var)

sql = ''' CREATE TABLE IF NOT EXISTS profiles
(main_id INT NOT NULL AUTO_INCREMENT, profile_id VARBINARY(255) NOT NULL UNIQUE %s, PRIMARY KEY (main_id)) ''' % columns
cur.execute(sql)

for table in conf.extra_tables:
    sql = ''' CREATE TABLE IF NOT EXISTS %s (id INT NOT NULL AUTO_INCREMENT, main_id INT NOT NULL, 
    %s VARCHAR(255) DEFAULT NULL, PRIMARY KEY (id), FOREIGN KEY(main_id) REFERENCES profiles(main_id)) ''' \
          % (table, table)
    cur.execute(sql)

con.commit()
con.close()
