import mysql.connector
import GV
import pandas as pd


def update_database(information, conditions):
    """
    """
    con = mysql.connector.connect(host='localhost', user=GV.MYSQL_USERNAME, passwd=GV.MYSQL_PASSWORD,
                                  auth_plugin='mysql_native_password')
    cur = con.cursor()
    cur.execute(''' USE okcupid_project ''')

    # SELECT columns
    select = 'SELECT '
    for info in information:
        if select != 'SELECT ':
            select += ', '
        if info in ['Age', 'Num_pics']:
            insert = (info, )
            select += 'profiles.%s' % insert
        else:
            insert = (info, info)
            select += '%s.%s' % insert

    # FROM tables
    tables = set(information + list(conditions.keys()))
    '''LEFT JOIN body_type ON profiles.main_id = body_type.main_id'''
    join = ' FROM profiles '
    for table in tables:
        if table not in ['Age', 'Num_pics']:
            join += "LEFT JOIN %s ON profiles.main_id = %s.main_id " % (table, table)

    # WHERE conditions
    where = ' WHERE '
    for parameter, condition in conditions.items():
        if where != ' WHERE ':
            where += ' AND '
        if parameter in ['Age', 'Num_pics']:
            insert = (parameter, condition[0], condition[1])
            where += '(profiles.%s BETWEEN %s AND %s)' % insert
        else:
            where += '('
            for cond in condition:
                insert = (parameter, parameter, cond)
                where += '%s.%s="%s" OR ' % insert
            where = where[:-4] + ')'

    sql = select + join + where
    print(sql)


    #
    # #
    # sql = '''SELECT profiles.main_id, profiles.Age, Tobacco.Tobacco
    # FROM profiles
    # LEFT JOIN body_type ON profiles.main_id = body_type.main_id
    # LEFT JOIN diet ON profiles.main_id = diet.main_id
    # LEFT JOIN drinks ON profiles.main_id = drinks.main_id
    # LEFT JOIN tobacco ON profiles.main_id = tobacco.main_id
    #
    # WHERE profiles.Age BETWEEN 20 AND 23'''

    #
    # sql = """
    # SELECT Gender.Gender, profiles.Age, Tobacco.Tobacco
    # FROM profiles
    # LEFT JOIN Tobacco ON profiles.main_id = Tobacco.main_id
    # LEFT JOIN Gender ON profiles.main_id = Gender.main_id
    # WHERE (Gender.Gender="Male" OR Gender.Gender="Woman") AND (profiles.Age BETWEEN 5 AND 100)
    # """


    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    #
    #
    #
    #
    # df = pd.read_sql(sql, con)
    # print(df)

    con.close()


information = ['Gender', 'Age', 'Tobacco']
conditions = {'Gender': ['Man', 'Woman'], 'Age': ['20', '30']}
update_database(information, conditions)

# sql = '''SELECT profiles.main_id, profiles.Age, Tobacco.Tobacco FROM
# body_type, diet, drinks,
# gender, profiles, tobacco
# WHERE profiles.Age BETWEEN 20 AND 30'''
# print(sql)
# cur.execute(sql)
# data = cur.fetchall()
# print(data)
