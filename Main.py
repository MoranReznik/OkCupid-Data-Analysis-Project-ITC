import EnterProfile
import ScrapeProfile as Scrape
import SiteLogin
import WaitForProfileToLoad
import UpdateDatabase
import logging
import CLIArguments

mode, profiles, required_details, number = CLIArguments.get_cli_arguments()


def main():

    counter = 0

    for main_profile_name, login_details in profiles.items():
        try:
            driver = SiteLogin.site_login(login_details)
        except Exception as e:
            print('Problem loading the site for %s. Please check your internet connection.' % main_profile_name)
            logging.exception(e)
            continue

        for i in range(1, number + 1):
            try:  # in case the program crushes, restart and complete the task
                print("%s: page number %s" % (main_profile_name, str(i)))
                profile_driver_unloaded, num_pics, profile_id = EnterProfile.enter_profile(driver)
                profile_driver_loaded = WaitForProfileToLoad.wait_for_profile_to_load(profile_driver_unloaded)
                driver, profile_data = Scrape.scrape_profile(
                    profile_driver_loaded, profile_id, num_pics, required_details)
                try:
                    UpdateDatabase.update_database(profile_data, main_profile_name)
                except Exception as e:
                    print('Please CreateDatabase before UpdateDatabase: ', e)
                    exit()
                counter += 1

            except Exception as e:
                print('Error: %s' % e)
                print('Problem loading the data. moving to the next person.')
                driver.close()
                driver = SiteLogin.site_login(login_details)
                logging.exception(e)

        driver.close()

    print('extracted data from ' + str(counter) + ' out of ' + str(number * len(profiles)) + ' profiles attempted')


if __name__ == '__main__':
    main()
