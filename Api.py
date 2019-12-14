import requests


def api(img_profile, img_compare):
    """ using api requests, we provide the url to the user's profile picture (which are not saved on the api server) and
    receive predicted data about the user's age, gender, facial expression and celebrity lookalike.
    In addition, we provide the urls to the rest of the user's pictures, and the API determines if all of them actually
    belong to the user.
    The data is organizes into a dictionary.

            Parameters
            ----------
            img_profile: string
                url of the profile pic

            img_compare: tuple
                tuple of the additional user's pictures

            Returns
            -------
            api_dict : dictionary
                dictionary that hold the predicted information about the profile
    """

    api_dict = {}

    # predict the gender, age and facial expression of the profile picture
    url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/detect"
    payload = "photo=" + img_profile
    headers = {'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
               'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
               'content-type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.json():
        result = response.json()[0]
        api_dict['pred_gender'] = result["gender"]["value"]
        api_dict['pred_age'] = round(result["age"])
        if result["expression"]:
            api_dict['pred_expression'] = result["expression"][0]["value"]

    # predict the celebrity lookalike of the profile picture
    url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/celebrity"
    querystring = {"photo": img_profile}
    payload = ""
    headers = {'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
               'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
               'content-type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    result = response.json()
    if result['result']:
        api_dict['pred_celeb'] = result['result'][0]['name']

    # Determines if the rest of the user's pictures actually belong to the user
    temp1 = "\"%s\", " * len(img_compare)
    temp2 = '[' + temp1[:-2] + ']'
    temp3 = temp2 % img_compare
    # temp3 = '["%s", "%s"]' % img_compare
    url = "https://macgyverapi-face-recognition-with-deep-learning-v1.p.rapidapi.com/"
    payload = '{"key": "free", "id": "5B3p2r8A", "data": {"known_image": ["%s"], "test_image": %s}}' % \
              (img_profile, temp3)
    headers = {'x-rapidapi-host': "macgyverapi-face-recognition-with-deep-learning-v1.p.rapidapi.com",
               'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
               'content-type': "application/json",
               'accept': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    result = response.json()
    if 'match' in result:
        api_dict['same'] = result['match']

    return api_dict
