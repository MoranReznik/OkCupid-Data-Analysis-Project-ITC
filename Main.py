import EnterProfile
import ScrapeProfile as scrape
import SiteLogin
import WaitForProfileToLoad
import GV
import logging
import json
from cryptography.fernet import Fernet
import CLIArguments

# privacy :  in order to encrypt the data to protects privacy of OkCupid Users, all the data in the
#      database will be encrypted.
#      the key will only be saved in a separate file in the repo, so even if the database will go to the
#      wrong hands, it will remain safe.
file = open('OkCupidKey', 'rb')  # opening the key file
key = file.read()
cipher = Fernet(key)
file.close()

profiles, required_details, number = CLIArguments.get_cli_arguents()


def main():

    counter = 0

    for prof_name, login_details in profiles.items():
        driver = SiteLogin.site_login(login_details)
        for i in range(1, number + 1):
            try:  # in case the program crushes, restart and complete the task
                print("%s: page number %s" % (prof_name, str(i)))
                profile_driver_unloaded, num_pics = EnterProfile.enter_profile(driver)
                profile_driver_loaded = WaitForProfileToLoad.wait_for_profile_to_load(profile_driver_unloaded)
                driver, profile_data = scrape.scrape_profile(profile_driver_loaded, num_pics, required_details)
                profile_data_byte = json.dumps(profile_data).encode('utf-8')
                encrypted_data = cipher.encrypt(profile_data_byte)
                GV.PROFILES[prof_name]["data"][i] = encrypted_data
                counter += 1

            except Exception as e:
                print('problem with loading the data. moving to the next person.')
                driver.close()
                driver = SiteLogin.site_login(login_details)
                logging.exception(e)

        driver.close()

    print('extracted data from ' + str(counter)+' out of ' + str(number * len(profiles)) + ' profiles attempted')


if __name__ == '__main__':
    main()
