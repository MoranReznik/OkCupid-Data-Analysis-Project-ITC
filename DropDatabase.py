# pip install mysql-connector-python
import mysql.connector

username = "root"
password = "KKkm73iaC2cnH3c#oMG$KD^JzA*f"


con = mysql.connector.connect(
    host='localhost', user=username, passwd=password, auth_plugin='mysql_native_password')
cur = con.cursor()

cur.execute(''' USE okcupid_project ''')
cur.execute(''' DROP DATABASE okcupid_project ''')

con.commit()
con.close()

# CreateDatabase.create_database()
