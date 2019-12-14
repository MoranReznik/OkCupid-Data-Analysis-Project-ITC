import mysql.connector
import pandas as pd


def read_database(mysql_cred, information, conditions):
    """ Reads from the database all the wanted information according to the wanted conditions

            mysql_cred
            ----------
            mysql_cred : list
                list with MYSQL username and password from the CLI arguments.

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

    profiles_columns = ['age', 'height', 'location', 'num_pics']

    # SELECT columns
    select = 'SELECT '
    if information:
        all_information = information.copy()
    else:
        # if user wants to read all the data, extract the list of all categories to output without the id
        all_information = ['age', 'height', 'location', 'num_pics']
        cur.execute("SHOW TABLES")
        categories = cur.fetchall()
        for category in categories:
            all_information += [category[0]]
        all_information.remove('profiles')

    for category in all_information:
        if select != 'SELECT ':
            select += ', '
        if category in profiles_columns:
            select += 'GROUP_CONCAT(DISTINCT(profiles.%s)) AS %s' % (category, category)
        else:
            select += 'GROUP_CONCAT(DISTINCT(%s.%s)) AS %s' % (category, category, category)

    # JOIN ON
    join = ' FROM profiles '
    tables = set(all_information + list(conditions.keys()))
    for table in tables:
        if table not in profiles_columns:
            join += "LEFT JOIN %s ON profiles.main_id = %s.main_id " % (table, table)

    # WHERE profiles.main_id IN (
    where_in = 'WHERE profiles.main_id IN (SELECT profiles.main_id as good_id FROM profiles '
    tables = set(conditions.keys())
    for table in tables:
        if table not in profiles_columns:
            where_in += "LEFT JOIN %s ON profiles.main_id = %s.main_id " % (table, table)

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
                    where += " '%s' IN (%s.%s) OR " % (cond, category, category)
                where = where[:-4] + ')'

    sql = select + join + where_in + where + ') GROUP BY profiles.main_id'
    df = pd.read_sql(sql, con)
    con.close()

    return df
