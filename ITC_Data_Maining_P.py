from ScrapingFuncs import *
NUMBER = 5
PROFILES = {"straight man": {"user": "itc.proje@gmail.com", "pass": "itc_pass4", "data": {}},
            "straight woman": {"user": "shirella111@gmail.com", "pass": "itcpass123", "data": {}}}


def main():
    counter = 0
    for profile_name, login_details in PROFILES.items():
        driver = site_login(login_details)
        for i in range(1, NUMBER + 1):
            try:  # in case the program crushes, restart and complete the task
                print("%s: page number %s" % (profile_name, str(i)))
                profile_driver_unloaded, num_pics = enter_profile(driver)
                profile_driver_loaded = wait_for_profile_to_load(profile_driver_unloaded)
                driver, PROFILES[profile_name]["data"][i] = scrape_profile(profile_driver_loaded, num_pics)
                counter += 1
            except:
                print('problem with loading the data. moving to the next person.')
                driver.close()
                driver = site_login(login_details)
        driver.close()

    print('extracted data from ' + str(counter)+' out of ' + str(NUMBER * len(PROFILES)) + ' profiles attempted')


if __name__ == '__main__':
    main()
