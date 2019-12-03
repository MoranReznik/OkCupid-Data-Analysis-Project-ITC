import mysql.connector
import GV


def update_database(profile_data):
    """ Updating MySQL database with all the date we scraped.
    The profile_id is encrypted to protects privacy of OkCupid Users.
    the key will be saved in a separate file in the repo, so even if the database will go to the
    wrong hands, it will remain safe.
    If the profile already exists in the database, add all new and updated data to the database.

            Parameters
            ----------
            profile_data : dictionary
                dictionary with all of the scraped data from the profile.

    """

    con = mysql.connector.connect(
        host='localhost', user=GV.MYSQL_USERNAME, passwd=GV.MYSQL_PASSWORD, auth_plugin='mysql_native_password')
    cur = con.cursor()
    cur.execute(''' USE okcupid_project ''')

    with open('OkCupidKey', 'rb') as file:
        key = file.read()
    profile_id = profile_data['Profile_id']

    # check if there is a duplicate profile_id
    sql = '''SELECT main_id, COUNT(Profile_id) from profiles WHERE Profile_id=AES_ENCRYPT("%s","%s")''' % \
          (profile_id, key)
    cur.execute(sql)
    main_id, exists = cur.fetchone()

    # first: if profile_id does't exist: add the encrypted unique profile_id to the profiles table and extract the PK
    if not exists:
        sql = '''INSERT INTO profiles (Profile_id) VALUES (AES_ENCRYPT("%s","%s"))''' % (profile_id, key)
        cur.execute(sql)

        cur.execute('SELECT LAST_INSERT_ID()')
        main_id = cur.fetchone()[0]

    for column, values in profile_data.items():
        # next: add the details relevant to the profiles table
        if column in ['Age', 'Height', 'Location', 'Num_pics']:
            sql = ''' UPDATE profiles SET %s = "%s" WHERE main_id = "%s" ''' % (column, values, main_id)
            cur.execute(sql)

        # finally: add the rest of the data to their table, where some of the data are str and some are lists of str.
        elif column != 'Profile_id':
            if type(values) == str:
                values = [values]
            for value in values:
                sql = '''INSERT INTO %s (main_id, %s) VALUES ("%s", "%s")''' % (column, column, main_id, value)
                cur.execute(sql)

    con.commit()
    con.close()
