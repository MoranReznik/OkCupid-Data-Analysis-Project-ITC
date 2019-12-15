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
            preds : dictionary
                dictionary that hold the predicted information about the profile
    """

    preds = {}

    # predict the gender, age and facial expression of the profile picture
    try:
        url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/detect"
        payload = "photo=" + img_profile
        headers = {'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
                   'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
                   'content-type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        result_1 = response.json()
        if result_1:
            preds['pred_gender'] = result_1[0]["gender"]["value"]
            preds['pred_age'] = round(result_1[0]["age"])
            if result_1[0]["expression"]:
                preds['pred_expression'] = result_1[0]["expression"][0]["value"]
    except Exception as e:
        print('Api response error: %s' % e)

    # predict the celebrity lookalike of the profile picture
    try:
        url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/celebrity"
        querystring = {"photo": img_profile}
        payload = ""
        headers = {'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
                   'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
                   'content-type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        result_2 = response.json()
        if result_2:
            if 'result' in result_2:
                if result_2['result']:
                    preds['pred_celeb'] = result_2['result'][0]['name']
    except Exception as e:
        print('Api response error: %s' % e)

    # Determines if the rest of the user's pictures actually belong to the user
    try:
        if img_compare:
            img_compare_string = ('[' + ("\"%s\", " * len(img_compare))[:-2] + ']') % img_compare
            url = "https://macgyverapi-face-recognition-with-deep-learning-v1.p.rapidapi.com/"
            payload = '{"key": "free", "id": "5B3p2r8A", "data": {"known_image": ["%s"], "test_image": %s}}' % \
                      (img_profile, img_compare_string)
            headers = {'x-rapidapi-host': "macgyverapi-face-recognition-with-deep-learning-v1.p.rapidapi.com",
                       'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
                       'content-type': "application/json",
                       'accept': "application/json"}
            response = requests.request("POST", url, data=payload, headers=headers)
            result_3 = response.json()
            if result_3:
                if 'match' in result_3:
                    preds['pred_pics_match'] = result_3['match']
    except Exception as e:
        print('Api response error: %s' % e)

    return preds
