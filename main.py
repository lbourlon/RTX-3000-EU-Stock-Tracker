import bot, util

import atexit, sys
from time import sleep


"""
    Defines a function to be run when the program is forcibly shut.
    This Function closes properly the webdriver before exiting
"""
def cleanup_function(web_driver):
    try:
        web_driver.quit()
    except:
        pass

    print("The program was closed earlier than expected")


#Main Function
def main(web_driver):
    nvidia_results, ldlc_results, materiel_results, top_achat_results, pc_componentes_results = ([], [], [], [], [])

    if(web_driver != None):
        print("- Checking nvidia.com")
        nvidia_results = bot.check_nvidia(util.nvidia_founders, web_driver)

        print("- Checking material.net")
        materiel_results = bot.check_materiel(util.materiel_urls, web_driver)

        web_driver.quit()
    else:
        print(" -- Skipping Javascript based sites")

    print("- Checking ldlc.com")
    ldlc_results = bot.check_ldlc(util.ldlc_urls) 

    print("- Checking topachat.com")
    top_achat_results = bot.check_top_achat(util.top_achat_url)

    print("- Checking pccomponentes.com")
    pc_componentes_results = bot.check_pc_componentes(util.pc_componentes_urls)

    full_list = ldlc_results + materiel_results + nvidia_results + top_achat_results + pc_componentes_results
    full_list = util.filter_results(full_list)
    util.print_results(full_list)




if __name__ == "__main__":
    while True:
        print("- Booting Selenium Firefox Webdriver")
        web_driver = bot.open_web_driver()

        atexit.register(cleanup_function, web_driver)

        main(web_driver)

        atexit.unregister(cleanup_function)
        print("- Sleeping for 15 seconds before running again")
        sleep(15)