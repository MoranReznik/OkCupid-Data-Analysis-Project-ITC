import argparse
import conf
import json


def get_cli_arguments():
    """ gets the relevant command line arguments and flags from the user.

            Returns
            -------
            if mode is 'read'
            args : list
                list of arguments: mode, [username, password], parameters to query based on as \
                a dict, information to show on profiles, name of csv file

            if mode is 'write'
            args : list
                list of arguments: mode, [username, password], number of profiles to scrape

             if mode is 'print'
            args : list
                list of arguments: mode, number of profiles to scrape
    """

    with open(conf.JSON) as json_file:
        dict_data = json.load(json_file)

    # creating the flags
    parser = argparse.ArgumentParser(description='scrape profiles from OkCupid')
    parser.add_argument('mode', type=str, help=conf.mode_help)
    parser.add_argument('--write_csv', type=str, help='name for csv file the query result will be written to')
    parser.add_argument('--no_api', action='store_true', help='not using api')
    parser.add_argument('-n', '--num', type=str, help='number of profiles to scrape for each profile type')
    for kind, options in dict_data.items():
        if kind == 'religion':
            parser.add_argument('-rl', '--religioness', nargs='+', help='religion to query based on.\
                         syntax: "label1 label2 label3". options: {}'.format(dict_data['religion']))
        elif kind == 'looking_for_connection':
            parser.add_argument('-lfc', '--connection_type', nargs='+', help='connection type to query based on.\
                         syntax: "label1 label2 label3". options: {}'.format(kind, dict_data['looking_for_connection']))
        else:
            parser.add_argument('-{}'.format(kind[0:3]), '--{}'.format(kind), nargs='+', help='{} to query based on.\
             syntax: "label1 label2 label3". options: {}'.format(kind, dict_data[kind]))
    parser.add_argument('-p', '--number_of_pics', nargs='+', help='number of pics in the profile, as a range: min max')
    parser.add_argument('-a', '--age', nargs='+', help='age of the profile, as a range: min max')
    parser.add_argument('-c', '--mysqlcreds', nargs='+',
                        help='username and password for mySQL server: username password')
    parser.add_argument('-i', '--information', nargs='+', help=conf.information_to_show_help)
    args = parser.parse_args()

    # checking mode is a valid value
    if args.mode not in ['read', 'write', 'print']:
        exp = 'please provide a valid mode to operate in! modes can be read, write or print.'
        raise Exception(exp)

    # if needed, making sure the valid number of profiles to scrape was given
    if args.mode in ['write', 'print']:
        if not args.num or not args.num.isnumeric():
            raise (Exception('please provide a number of profiles to scrape'))

    # if needed, make sure username and password were provided:
    if args.mode in ['write', 'read']:
        if not args.mysqlcreds or len(args.mysqlcreds) != 2:
            raise (Exception('please enter valid username and password'))

    # make sure values to scrape by are valid
    kinds = dict_data.keys()
    if args.mode == 'read':
        for kind in kinds:
            if kind == 'religion':
                kind = 'religioness'
            elif kind == 'looking_for_connection':
                kind = 'connection_type'
            if getattr(args, kind):
                if kind == 'religioness':
                    valid_labels = dict_data['religion']
                elif kind == 'connection_type':
                    valid_labels = dict_data['connection_type']
                else:
                    valid_labels = dict_data[kind]
                for label in getattr(args, kind):
                    if label not in valid_labels:
                        raise (Exception('label {} not an option in detail kind {}'.format(label, kind)))

        if args.number_of_pics:
            if len(args.number_of_pics) != 2 or not args.number_of_pics[0].isnumeric() or \
                    not args.number_of_pics[1].isnumeric():
                raise (Exception('please provide a valid number of pictures as range! (syntax: "min max")'))

        if args.age:
            if len(args.age) != 2 or not args.age[0].isnumeric() or not args.age[1].isnumeric():
                raise (Exception('please provide a valid age as range! (syntax: "min max")'))

    # make sure column to show are valid
    if args.mode == 'read':
        if args.information:
            for info in args.information:
                if info not in kinds and info not in ['num_pics', 'age', 'height', 'location', 'religion_importance']:
                    raise (Exception('detail kind {} does not exist'.format(info)))

    # arrange dict of parameters to query database based on
    conditions = {}
    if args.mode == 'read':
        for kind in kinds:
            if kind == 'religion':
                kind = 'religioness'
            elif kind == 'looking_for_connection':
                kind = 'connection_type'
            if getattr(args, kind):
                conditions[kind] = getattr(args, kind)
    if args.number_of_pics:
        conditions['num_pics'] = args.number_of_pics
    if args.age:
        conditions['age'] = args.age

    if 'religioness' in conditions:
        conditions['religion'] = conditions.pop('religioness')
    if 'connection_type' in conditions:
        conditions['looking_for_connection'] = conditions.pop('connection_type')

    if args.no_api is True:
        api = False
    else:
        api = True

    if args.mode == 'read':
        return [args.mode, args.mysqlcreds, conditions, args.information, args.write_csv]
    elif args.mode == 'write':
        return [args.mode, int(args.num), args.mysqlcreds, api]
    else:
        return [args.mode, int(args.num), api]
