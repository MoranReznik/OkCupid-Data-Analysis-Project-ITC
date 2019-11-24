import DictData

def find_kind_of_detail(string):
    """helper func for the scrape func. in order to place a single detail on a person
    in the right key, we need to know to what category this detail belongs to
    possible categories are specified in the scrape func's docstring"""

    for key, values in DictData.choices.items():
        for value in values:
            if value.lower() in string.lower():
                return key