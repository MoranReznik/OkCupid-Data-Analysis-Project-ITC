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
                the input string parsed to a more human readable form
    """

    if kind == 'speaks':
        detail = detail.replace(',', '')
        languages = detail.split(' ')
        if 'Speaks' in languages:
            languages.remove('Speaks')
        if 'and' in languages:
            languages.remove('and')
        if 'some' in languages:
            languages.remove('some')
        if '' in languages:
            languages.remove('')
        return languages

    elif kind == 'religion':
        detail = detail.split(' (')
        if len(detail) > 1:
            return [detail[0],  detail[1][:-1]]
        else:
            return [detail[0][1:]]

    elif kind == 'height':
        detail = detail[1:-2]
        return detail

    elif kind == 'looking_for_gender':
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
