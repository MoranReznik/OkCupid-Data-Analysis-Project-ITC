import EnterProfile
import ReadDatabase
import ScrapeProfile as Scrape
import SiteLogin
import WaitForProfileToLoad
import UpdateDatabase
import logging
import CLIArguments
import conf
import mysql.connector


def main():

    counter = 0

    parameters = CLIArguments.get_cli_arguments()
    mode = parameters[0]

    if mode in ['print', 'write']:
        num_to_scrape = parameters[1]
        for main_profile_name, login_details in conf.PROFILES.items():
            try:
                driver = SiteLogin.site_login(login_details)
            except Exception as e:
                print('Problem loading the site for %s. Please check your internet connection.' % main_profile_name)
                logging.exception(e)
                continue

            for i in range(1, num_to_scrape + 1):
                try:  # in case the program crushes, restart and complete the task
                    print("%s: page number %s" % (main_profile_name, str(i)))
                    profile_driver_unloaded, num_pics, profile_id = EnterProfile.enter_profile(driver)
                    profile_driver_loaded = WaitForProfileToLoad.wait_for_profile_to_load(profile_driver_unloaded)
                    driver, profile_data = Scrape.scrape_profile(
                        profile_driver_loaded, profile_id, num_pics, mode)
                    if mode == 'write':
                        mysql_cred = parameters[2]
                        try:
                            UpdateDatabase.update_database(mysql_cred, profile_data)
                        except mysql.connector.Error as err:
                            print("Something went wrong: {}".format(err))
                    counter += 1

                except Exception as e:
                    print('Error: %s' % e)
                    print('Problem loading the data. moving to the next person.')
                    driver.close()
                    driver = SiteLogin.site_login(login_details)
                    logging.exception(e)

            driver.close()

        print('extracted data from ' + str(counter) + ' out of ' + str(num_to_scrape * len(conf.PROFILES)) +
              ' profiles attempted')

    if mode == 'read':
        _, mysql_cred, conditions, information, csv_name = parameters
        df = ReadDatabase.read_database(mysql_cred, information, conditions)
        if csv_name:
            df.to_csv(csv_name)
        else:
            print(df)


if __name__ == '__main__':
    main()
