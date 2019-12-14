import requests


def api(img_profile, img_compare):
    """
    input:
    img_profile = url of the profile pic (string)
    img_compare = urls of the additional pics (tuple of strings)

    output:
    predicted gender and age, user expression, user celeb lookalike,
    and True/False if rest of images actually belong to the user
    """

    # gender, age, expression
    url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/detect"
    payload = "photo=" + img_profile
    headers = {'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
               'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
               'content-type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    result = response.json()[0]
    gender = result["gender"]["value"]
    age = round(result["age"])
    expression = result["expression"][0]["value"]


    # celeb
    url = "https://luxand-cloud-face-recognition.p.rapidapi.com/photo/celebrity"
    querystring = {"photo": img_profile}
    payload = ""
    headers = {'x-rapidapi-host': "luxand-cloud-face-recognition.p.rapidapi.com",
               'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
               'content-type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    result = response.json()
    celeb = result['result'][0]['name']


    # verifie
    temp1 = "\"%s\", "*2
    temp2 = '[' + temp1[:-2] + ']'
    temp3 = temp2 % img_compare
    # temp3 = '["%s", "%s"]' % img_compare
    url = "https://macgyverapi-face-recognition-with-deep-learning-v1.p.rapidapi.com/"
    payload = '{"key": "free", "id": "5B3p2r8A", "data": {"known_image": ["%s"], "test_image": %s}}' % (img_profile, temp3)
    headers = {'x-rapidapi-host': "macgyverapi-face-recognition-with-deep-learning-v1.p.rapidapi.com",
               'x-rapidapi-key': "63130e96b1msh90c1eaf79ef5036p11e9cajsndb50d6caa382",
               'content-type': "application/json",
               'accept': "application/json"}
    response = requests.request("POST", url, data=payload, headers=headers)
    result = response.json()
    same = result['match']

    return gender, age, expression, celeb, same


# # profile pic: from here we predict the gender, age, expression and celeb lookalike
# img_profile = "https://cdn.okccdn.com/php/load_okc_image.php/images/225x225/225x225/80x0/559x479/0/13260960704398444995.jpeg"
#
# # rest of the pics: we compare these to the profile pic to make sure they all belong to the user
# img_compare = ("https://cdn.okccdn.com/php/load_okc_image.php/images/225x225/225x225/0x80/640x720/0/1906781724375760774.jpeg",
#                "https://cdn.okccdn.com/php/load_okc_image.php/images/225x225/225x225/0x75/640x715/0/8764547662252339471.jpeg")
#
# gender, age, expression, celeb, same = api(img_profile, img_compare)
# print(gender, age, expression, celeb, same)
