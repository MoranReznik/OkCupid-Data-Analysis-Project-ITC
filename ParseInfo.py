def parse_info(data, details_temp, dict_data):
    """ gets the data about the user and organizes it into a dictionary

            Parameters
            ----------
            data : dictionary
                dictionary that hold some information about the profile

            details_temp: list
                list of unorganized strings that contain information about the user

            dict_data: dictionary
                a dictionary that contains all of the values possible for each category of detail


            Returns
            -------
            data : dictionary
                dictionary that hold ALL information about the profile
    """

    dets = []

    # languages that the user speaks
    for details in details_temp:
        if 'speaks' in details:
            for value in dict_data['speaks']:
                if value in details:
                    if 'speaks' not in data:
                        data['speaks'] = []
                    data['speaks'] += [value]

    # separating the data into a list. this is done after taking care of the languages since the languages sometimes
    # contain commas of their own
    for detail_list in details_temp:
        details = detail_list.split(',')
        dets += details

    # for each detail on the profile, place into a data
    for i, det in enumerate(dets):

        # cleaning the detail
        det = det.strip(' ')
        det = det.replace('and ', '')
        det = det.replace('attended ', '')

        # height
        if 'cm' in det:
            data['height'] = det

        # strings that starts with "looking for" have a special structure so we take care of them here
        elif 'looking for ' in det:

            data['looking_for_gender'] = []
            data['looking_for_connection'] = []

            if 'non' in det:
                data['relationship_type'] = 'non-monogamous'
            else:
                data['relationship_type'] = 'monogamous'

            for g in ['women', 'people']:
                if g in det:
                    if 'looking_for_gender' not in data:
                        data['looking_for_gender'] = []
                    data['looking_for_gender'] += [g]

            man_ind = det.find('men')  # this code takes care of the problem that the word man is part of the word
            if man_ind != -1:          # women
                if det[man_ind - 1] != 'o':
                    data['looking_for_gender'] = []
                    data['looking_for_gender'] += ['man']


            for c in ['long', 'short', 'friends', 'hookups']:
                if c in det:
                    if 'looking_for_connection' not in data:
                        data['looking_for_connection'] = []
                    data['looking_for_connection'] += [c]

        # taking care of all the regular kind of details
        else:
            for key, value in dict_data.items():
                if det in value and key != 'speaks':  # make sure speaks is not overwritten
                    data[key] = det

                for rel in dict_data['religion']:  # taking care of the religion, which has a special structure
                    if rel in det:
                        if '(' in det:
                            r = det.split('(')
                            data['religion'] = r[0].strip(' ')
                            data['religion_importance'] = r[1].strip(' ').strip(')')
                        else:
                            data['religion'] = rel

        if 'drink' in det:  # drinks also appears different in dict_data and in the site, so we fix it here
            if "doesn't drink" in det:
                data['drink'] = 'never drinks'
            elif 'often' in det:
                data['drink'] = 'drinks often'

        if 'open to non-monogamy' in det: # taking care of the special case where the non-monogamy is stated separately
            data['relationship_type'] = 'non-monogamous'

    return data
