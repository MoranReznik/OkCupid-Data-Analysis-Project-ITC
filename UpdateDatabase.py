import mysql.connector
import GV


def update_database(profile_data, scraper_profile_name):
    """ Updating MySQL database with all the date we scraped.
    The profile_id is encrypted to protects privacy of OkCupid Users.
    the key will be saved in a separate file in the repo, so even if the database will go to the
    wrong hands, it will remain safe.
    If the profile already exists in the database, since the details might have been updated,
    delete it from the database and re-add it.

            Parameters
            ----------
            profile_data : dictionary
                dictionary with all of the scraped data from the profile.

            scraper_profile_name : str
                the name of the current scraping profile (specified in the GV file)
    """

    con = mysql.connector.connect(
        host='localhost', user=GV.MYSQL_USERNAME, passwd=GV.MYSQL_PASSWORD, auth_plugin='mysql_native_password')
    cur = con.cursor()
    cur.execute(''' USE okcupid_project ''')

    with open('OkCupidKey', 'rb') as file:
        key = file.read()
    profile_id = profile_data['Profile_id']

    # check if there is a duplicate profile_id
    insert = (profile_id, key)
    sql = '''SELECT main_id, COUNT(Profile_id) from profiles WHERE Profile_id=AES_ENCRYPT("%s","%s")''' % insert
    cur.execute(sql)
    main_id, exists = cur.fetchone()

    # if there is a duplicate, remove its data from profiles table after removing it from the rest of the the tables
    if exists:
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        tables.append(tables.pop(tables.index(('profiles',))))  # move profiles to the end of the list
        for table in tables:
            sql = ''' DELETE FROM %s WHERE main_id="%s" ''' % (table[0], main_id)
            cur.execute(sql)

    # first: add the encrypted unique profile_id and the main_profile_name to the profiles table and extract the PK
    insert = (profile_id, key, scraper_profile_name)
    sql = '''INSERT INTO profiles (Profile_id, Scraper_profile) VALUES (AES_ENCRYPT("%s","%s"), "%s")''' % insert
    cur.execute(sql)

    cur.execute('SELECT LAST_INSERT_ID()')
    main_id = cur.fetchone()[0]

    for column, value in profile_data.items():

        # next: add the details relevant to the profiles table
        if column in ['Age', 'Height', 'Location', 'Num_pics']:
            insert = (column, value, main_id)
            sql = ''' UPDATE profiles SET %s = "%s" WHERE main_id = "%s" ''' % insert
            cur.execute(sql)

        # finally: add the rest of the data to their table, where some of the data are str and some are lists of str.
        elif column != 'Profile_id':
            values = value
            if type(value) == str:
                values = [value]
            for val in values:
                insert = (column, column, main_id, val)
                sql = '''INSERT INTO %s (main_id, %s) VALUES ("%s", "%s")''' % insert
                cur.execute(sql)

    con.commit()
    con.close()
