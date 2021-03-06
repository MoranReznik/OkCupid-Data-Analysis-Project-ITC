import mysql.connector
import conf


def update_database(mysql_cred, profile_data):
    """ Updating MySQL database with all the date we scraped.
    The profile_id is encrypted to protects privacy of OkCupid Users.
    the key will be saved in a separate file in the repo, so even if the database will go to the
    wrong hands, it will remain safe.
    If the profile already exists in the database, add all new and updated data to the database.

            Parameters
            ----------
            mysql_cred : list
                list with MYSQL username and password from the CLI arguments.

            profile_data : dictionary
                dictionary with all of the scraped data from the profile.

    """

    username, password = mysql_cred
    con = mysql.connector.connect(host='localhost', user=username, passwd=password,
                                  auth_plugin='mysql_native_password')
    cur = con.cursor()
    cur.execute(''' USE okcupid_project ''')

    with open('OkCupidKey', 'rb') as file:
        key = file.read()
    profile_id = profile_data['profile_id']

    # check if there is a duplicate profile_id
    sql = '''SELECT main_id, COUNT(Profile_id) from profiles WHERE Profile_id=AES_ENCRYPT("%s","%s")''' % \
          (profile_id, key)
    cur.execute(sql)
    main_id, exists = cur.fetchone()

    if exists:
        print('This profiles was already in the database. Updating profile..')

    # first: if profile_id does't exist: add the encrypted unique profile_id to the profiles table and extract the PK
    if not exists:
        sql = '''INSERT INTO profiles (Profile_id) VALUES (AES_ENCRYPT("%s","%s"))''' % (profile_id, key)
        cur.execute(sql)

        cur.execute('SELECT LAST_INSERT_ID()')
        main_id = cur.fetchone()[0]

    for column, values in profile_data.items():
        # next: add the details relevant to the profiles table
        if column in conf.profiles_columns:
            sql = ''' UPDATE profiles SET %s = "%s" WHERE main_id = "%s" ''' % (column, values, main_id)
            cur.execute(sql)

        # finally: add the rest of the data to the relevant table
        elif column and column != 'profile_id':  # in case column for some reason is an empty list..
            if type(values) == str:
                values = [values]
            if exists:
                # first delete old values and then insert new values (since there may be a different amount of
                # old and new values)
                sql = ''' DELETE FROM %s WHERE main_id="%s" ''' % (column, main_id)
                cur.execute(sql)
            for value in values:
                sql = '''INSERT INTO %s (main_id, %s) VALUES ("%s", "%s")''' % (column, column, main_id, value)
                cur.execute(sql)

    con.commit()
    con.close()
