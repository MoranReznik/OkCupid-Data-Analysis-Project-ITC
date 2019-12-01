import argparse
import GV


def get_cli_arguments():
    """ gets the relevant command line flags from the user.

            Returns
            -------
            args : ArgumentParser objects
                includes the different flags specified by the user.
    """

    # creating the flags
    parser = argparse.ArgumentParser(description='scrape profiles from OkCupid')
    parser.add_argument('num', type=int, help='number of profiles to scrape for each profile type')
    parser.add_argument('-p', '--profiles', nargs='+', help=GV.profiles_help)
    parser.add_argument('-i', '--information', nargs='+', help=GV.information_help)
    args = parser.parse_args()

    # checking number of profiles to scrape is a valid integer - raise exception if not
    if not isinstance(args.num, int):
        exp = 'please provide an integer number as the amount of profiles to scrape!'
        raise Exception(exp)

    # checking all profiles types given are valid - raise exception if not
    if args.profiles is not None:
        for profile_type in args.profiles:
            if profile_type not in GV.PROFILES.keys():
                exp = 'profile type {} not valid! check the help for this flag for available types'.format(profile_type)
                raise Exception(exp)

    # creating a dict with only the required profile types, if necessary
    profiles = {}
    if args.profiles is not None:
        for prof_name, login_details in GV.PROFILES.items():
            if prof_name in args.profiles:
                profiles[prof_name] = login_details
    else:
        profiles = GV.PROFILES

    # checking all information kinds types given are valid - raise exception if not
    required_details = GV.required_details
    if args.information is not None:
        for kind in args.information:
            if kind not in required_details:
                exp = 'information kind {} not valid! check the help for this flag for available types'.format(kind)
                raise Exception(exp)
    # creating a list with only the required details kinds, if necessary
    if args.information is not None:
        required_details = args.information

    return profiles, required_details, args.num
