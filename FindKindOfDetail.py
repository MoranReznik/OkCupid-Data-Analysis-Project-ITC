import json

with open('choices.json') as json_file:
    DICT_DATA = json.load(json_file)
    for k, v in DICT_DATA.items():
        lower_k = k.lower()
        DICT_DATA[lower_k] = DICT_DATA.pop(k)
        values = []
        for i in v:
            values.append(i.lower())
    DICT_DATA[lower_k] = values

def find_kind_of_detail(string):
    """ helper func for the scrape func. in order to place a single detail on a person
    in the right key, we need to know to what category this detail belongs to
    possible categories are specified in the scrape func's docstring

            Parameters
            ----------
            string : string
                the detail of which we want know the category of


            Returns
            -------
            key : string
                the category of the input detail
    """

    for key, values in DICT_DATA.items():
        for value in values:
            if value.lower() in string.lower():
                if key == 'status' and 'Looking' not in string:
                    return 'status'
                elif key == 'status':
                    continue
                return key
