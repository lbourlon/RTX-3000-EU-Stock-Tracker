import bot
import util


targeted_url_ldlc = util.targeted_urls_ldlc[0]
nvidia_founders_url = util.nvidia_founders


if __name__ == "__main__":
    nvidia_results, ldlc_results, materiel_results, top_achat_results, pc_componentes_results = ([], [], [], [], [])

    print("- Booting Selenium Firefox Webdriver")
    web_driver = bot.open_web_driver()

    if(web_driver != None):
        print("- Checking nvidia.com")
        nvidia_results = bot.check_nvidia(nvidia_founders_url, web_driver)

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


    input("Press 'Enter' to exit the program")