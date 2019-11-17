from ScrapingFuncs import *
NUMBER = 3


def main():
    man_data = {}
    driver = site_login('women')
    counter = 0
    for i in range(NUMBER):
        try:  # in case the program crushes, restart and complete the task
            print("Page number %s" % str(i + 1))
            profile_driver_unloaded = enter_profile(driver)
            profile_driver_loaded = wait_for_profile_to_load(profile_driver_unloaded)
            driver, man_data[i + 1] = scrape_profile(profile_driver_loaded)
            counter += 1
        except:
            print('problem with loading the data. moving to the next person.')
            driver.close()
            driver = site_login('women')
    driver.close()

    woman_data = {}
    driver = site_login('men')
    for i in range(NUMBER):
        try:  # in case the program crushes, restart and complete the task
            print("Page number %s" % str(i + 1))
            profile_driver_unloaded = enter_profile(driver)
            profile_driver_loaded = wait_for_profile_to_load(profile_driver_unloaded)
            driver, woman_data[i + 1] = scrape_profile(profile_driver_loaded)
            counter += 1
        except:
            print('problem with loading the data. moving to the next person.')
            driver.close()
            driver = site_login('men')
    print('extracted data from ' + str(counter)+' out of '+ str(NUMBER*2) + ' profiles attempted')
    driver.close()

if __name__ == '__main__':
    main()
