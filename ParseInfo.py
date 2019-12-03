def parse_info(detail, kind):
    """ gets a detail and its associated detail kind, and parse it to a more human readable form

            Parameters
            ----------
            detail : string
                the information about the person
            kind: string
                the category this info belongs to


            Returns
            -------
            detail : string
                the input string preased to a more human readable form
    """

    if kind == 'speaks':

        detail = detail[7:]  # remove the word speaks from the string
        languages = detail.replace('and', ',')
        languages = languages.replace(', some', ',')
        languages = languages.split(',')
        for index, language in enumerate(languages):
            languages[index] = language.strip(' ')
        return languages

    elif kind == 'Religion':
        detail = detail.split(' (')
        if len(detail) > 1:
            return [detail[0],  detail[1][:-1]]
        else:
            return detail[0]

    elif kind == 'Height':
        detail = detail[:-2]
        return detail

    elif kind == 'Looking_for_gender':
        detail = detail[12:]
        detail = detail.replace("short-term", 'short')
        detail = detail.replace("long-term", 'long')
        detail = detail.replace("and new", '')
        detail = detail.replace(".", '')
        detail = detail.split(' ')
        connection = [i for i in detail if i in ["short", "long", "hookups", "friends"]]
        gender = [i for i in detail if
                  i in ['men', 'women', 'agenders', 'androgynes', 'bigenders', 'cis Men', 'cis Women',
                        'genderfluids', 'genderqueers', 'genders nonconforming', 'hijras', 'intersexes',
                        'non-binaries', 'others', 'pangenders', 'transfeminines', 'transgenders',
                        'transmasculines', 'transsexuals', 'trans Men', 'trans Women', 'two Spirits']]
        return [gender, connection]

    elif kind:
        return detail.strip()
