import mysql.connector
import GV
import pandas as pd


def read_database(mysql_cred, information, conditions):
    """ Reads from the database all the wanted information according to the wanted conditions

            Parameters
            ----------
            information : list
                wanted categories to output
            conditions : dictionary
                according to which conditions to output


            Returns
            -------
            df : Pandas DataFrame
                DataFrame consisting of wanted categories according to the conditions
    """

    username, password = mysql_cred
    con = mysql.connector.connect(host='localhost', user=username, passwd=password,
                                  auth_plugin='mysql_native_password')
    cur = con.cursor()
    cur.execute(''' USE okcupid_project ''')

    # SELECT columns
    select = 'SELECT '
    if information:
        all_information = information.copy()
    if not information:  # Extract the list of all categories to output
        cur.execute("SHOW TABLES")
        categories = cur.fetchall()
        all_information = ['age', 'height', 'location', 'num_pics']
        for category in categories:
            all_information += [category[0]]
        all_information.remove('profiles')

    for category in all_information:
        if select != 'SELECT ':
            select += ', '
        if category in ['age', 'height', 'location', 'num_pics']:
            select += 'profiles.%s' % (category, )
        else:
            select += '%s.%s' % (category, category)

    # JOIN ON
    join = ' FROM profiles '
    tables = set(all_information + list(conditions.keys()))
    for table in tables:
        if table not in ['age', 'height', 'location', 'num_pics']:
            join += "LEFT JOIN %s ON profiles.main_id = %s.main_id " % (table, table)

    # WHERE condition
    if not conditions:
        where = ''
    else:
        where = ' WHERE '
        for category, condition in conditions.items():
            if where != ' WHERE ':
                where += ' AND '
            if category in ['age', 'num_pics']:
                where += '(profiles.%s BETWEEN %s AND %s)' % (category, condition[0], condition[1])
            else:
                where += '('
                for cond in condition:
                    where += '%s.%s="%s" OR ' % (category, category, cond)
                where = where[:-4] + ')'

    sql = select + join + where
    df = pd.read_sql(sql, con)
    con.close()

    return df


#
# info = ['gender', 'age', 'tobacco', 'drugs', 'num_pics']
# info = ['all']
# cond = {}
#
# cond = {'gender': ['man', 'woman'], 'age': ['20', '30'], 'tobacco': ["doesn't smoke cigarettes"]}
# dff = read_database(info, cond)
# print(dff)
