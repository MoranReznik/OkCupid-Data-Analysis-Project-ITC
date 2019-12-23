import argparse
import mysql.connector


""" deleting MySQL database """

# creating the flags
parser = argparse.ArgumentParser(description='username and password for deleting of mySQL database')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='password')
args = parser.parse_args()


con = mysql.connector.connect(
    host='localhost', user=args.username, passwd=args.password, auth_plugin='mysql_native_password')
cur = con.cursor()

cur.execute(''' USE okcupid_project ''')
cur.execute(''' DROP DATABASE okcupid_project ''')

con.commit()
con.close()
