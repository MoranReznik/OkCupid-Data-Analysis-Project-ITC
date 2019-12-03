import mysql.connector
import GV

con = mysql.connector.connect(host='localhost', user=GV.MYSQL_USERNAME, passwd=GV.MYSQL_PASSWORD,
                              auth_plugin='mysql_native_password')
cur = con.cursor()
cur.execute(''' USE okcupid_project ''')

sql2 = 'SHOW COLUMNS FROM okcupid_project.profiles'
sql3 = 'SELECT * FROM okcupid_project.education'
cur.execute('DROP DATABASE okcupid_project')
data = cur.fetchall()

parameter = 'Gender'
condition = 'Woman'
insert = (parameter, condition)
sql = ''' SELECT main_id FROM profiles WHERE %s=%s '''
cur.execute(sql)
main_id = cur.fetchone()[0]


cur.execute("SHOW TABLES")
tables = cur.fetchall()
for table in tables:
    if table[0] != 'profiles':
        insert = (parameter, condition)
        sql = ''' SELECT %s FROM %s WHERE %s=%s '''

    else:
        sql = ''' SELECT * FROM %s ''' % table[0]
    cur.execute(sql)
    data = cur.fetchall()
    print(table[0] + ':   ', data, '\n')

con.commit()
con.close()


