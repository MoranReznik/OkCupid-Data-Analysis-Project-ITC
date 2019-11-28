import json

with open('choices.json') as json_file:
    DICTDATA = json.load(json_file)

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

    for key, values in DICTDATA.items():
        for value in values:
            if value.lower() in string.lower():
                return key
