def find_image_url(soup):
    """ gets urls of profile picutres

            Parameters
            ----------
            soup : a soup object
                with the information from the profile


            Returns
            -------
            links : list
                a list of urls to all of the profile pictures
    """

    links = []

    urls = soup.findAll('img')
    # extracting the profile image links
    for url in urls:
        url = str(url)
        if 'profile' in url:  # make sure it is a profile picutre
            src_ind = url.find('src')
            link = url[src_ind + 5:-3]  # removing all chars that are not part of the url
            links.append(link)
    links = links[1:]  # the first profile picture is ours

    return links
