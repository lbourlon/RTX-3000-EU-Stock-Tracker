import requests
from selenium import webdriver
from lxml import html
import util
from util import exception_safe

@exception_safe
def check_ldlc(urls):
    out_results = []
    for url in urls:
        tree = util.get_tree(url)

        nb_resultats = tree.xpath('/html/body/div[3]/div/div[3]/div[1]/div/div[2]/div[1]/div[1]/text()')[0]
        nb = util.make_num(nb_resultats)
        
        results = []

        for i in range(1,int(nb) + 1):
            prix_ = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[4]/div[1]/div/text()")[0][0:-1]
            prix = util.make_num(prix_)
            if(int(prix) >= 850):
                continue

            titre = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[1]/div[1]/h3/a/text()")[0]
            if('water' in titre.lower() or 'hydro' in titre.lower()):
                continue
            
            dispo = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[3]/div/div[2]/div/span/text()")[0]

            dispo_p2 = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[3]/div/div[2]/div/span/em/text()")
            if len(dispo_p2) >= 1 :
                dispo = dispo + ' ' + dispo_p2[0]

            results.append(('LDLC.com    ' + util.clean_string(titre), util.clean_string(dispo), util.clean_string(prix)))

        out_results += results
        
    return out_results

@exception_safe
def check_top_achat(urls):
    out_results = []
    for url in urls:
        tree = util.get_tree(url)

        nb_resultats = tree.xpath('//*[@id="content"]/nav[1]/ul/li[4]/text()')[0]
        nb = util.make_num(nb_resultats)
        results = []

        liste_prix_ = tree.xpath("//section[@class = 'produits list']//div[@itemprop= 'price']/text()")
        liste_titres = tree.xpath("//section[@class = 'produits list']//div[@class = 'libelle']/a/h3/text()")
        liste_dispos =  tree.xpath("//section[@class = 'produits list']//section[last()]/@class")
        
        for i in range(0,int(nb)):
            prix_ = liste_prix_[i][0:-4]
            prix = util.make_num(prix_)
            if(int(prix) >= 850):
                continue

            titre = liste_titres[i]
            geforce_ad = " + 1 an d'abonnement GeForce Now offert ! ".lower()
            call_of_ad = "+ Call of Duty: Black Ops Cold War offert ! ".lower()
            if('water' in titre.lower() or 'hydro' in titre.lower()):
                continue
            elif(geforce_ad in titre.lower()):
                titre = titre[0:len(titre) - len(geforce_ad)] 
            elif(call_of_ad in titre.lower()):
                titre = titre[0:len(titre) - len(call_of_ad)]

            raw_dispo = liste_dispos[i] 
            dispo = ""
            if(raw_dispo == 'en-rupture'):
                dispo = 'Rupture'
            elif(raw_dispo == 'dispo-sous-7-jours'):
                dispo = 'sous 7 jours'
            elif(raw_dispo == 'dispo-entre-7-15-jours'):
                dispo = 'entre 7-15 jours'
            elif(raw_dispo == 'dispo-plus-15-jours'):
                dispo =  '+ de 15 jours'
            else:
                dispo = raw_dispo


            results.append(('topachat.com    ' + util.clean_string(titre), dispo, util.clean_string(prix)))
        out_results += results

    return out_results

def check_pc_componentes(url):
    print(url)
    tree = util.get_tree(url)

    list = tree.xpath(f"//header[@class = 'c-product-card__header']")
    print(list)
    
    results = []

    for i in range(1,int(nb) + 1):
        prix_ = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[4]/div[1]/div/text()")[0][0:-1]
        prix = util.make_num(prix_)
        if(int(prix) >= 850):
            continue

        titre = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[1]/div[1]/h3/a/text()")[0]
        if('water' in titre.lower() or 'hydro' in titre.lower()):
            continue
        
        dispo = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[3]/div/div[2]/div/span/text()")[0]

        dispo_p2 = tree.xpath(f"//*[@id='listing']//*[@data-position='{i}']/div[2]/div[3]/div/div[2]/div/span/em/text()")
        if len(dispo_p2) >= 1 :
            dispo = dispo + ' ' + dispo_p2[0]

        results.append(('pccomponents.com    ' + util.clean_string(titre), util.clean_string(dispo), util.clean_string(prix)))

        return results

        
@exception_safe
def ldlc_targeted(url):
    tree = util.get_tree(url)

    name = tree.xpath("/html/body/div[3]/div[2]/div[1]/h1/text()")[0]
    dispo = tree.xpath("/html/body/div[3]/div[2]/div[2]/div[3]/aside/div[4]/div[1]/div[2]/div/span/text()")[0]
    prix_ = tree.xpath("/html/body/div[3]/div[2]/div[2]/div[3]/aside/div[1]/div/text()")[0][0:-1]

    prix = util.make_num(prix_)
    return (util.clean_string(name), util.clean_string(dispo), util.clean_string(prix))




#---------------Functions where the sites require javascript-----------------

@exception_safe
def open_web_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path ='C:/Users/lbourlon/Documents/geckodriver.exe', options = options)

    return driver


@exception_safe
def check_nvidia(url, web_driver):
    web_driver.get(url)
    num = int(util.make_num(web_driver.find_element_by_xpath('/html/body/app-root/product/div[1]/div[1]/div[2]/div/suggested-product/div/div').text))
    results = []                       
    name = web_driver.find_element_by_xpath('//featured-product/div/div/div[2]/div[2]/h2').text
    dispo = web_driver.find_element_by_xpath('//featured-product/div/div/div[2]/div[3]/div[1]/div[2]/a').text
    prix = util.make_num(web_driver.find_element_by_xpath('//featured-product/div/div/div[2]/div[3]/div[1]/div[1]/div/span[1]').text)

    if dispo ==  "RUPTURE DE STOCK":
        dispo = "Rupture"

    results.append(("FE    " + util.clean_string(name), util.clean_string(dispo), util.clean_string(prix)))

    if num == None:
        num = 2

    for i in range(1,num):
        name = web_driver.find_element_by_xpath(f'//*[@id="resultsDiv"]/div/div[{i}]/div[2]/h2').text
        dispo = web_driver.find_element_by_xpath(f'//*[@id="resultsDiv"]/div/div[{i}]/div[3]/div[2]/div[2]/a').text
        prix = util.make_num(web_driver.find_element_by_xpath(f'//*[@id="resultsDiv"]/div/div[{i}]/div[3]/div[2]/div[1]/div/span[1]').text)

        if dispo ==  "RUPTURE DE STOCK":
            dispo = "Rupture"

        results.append(("FE    " + util.clean_string(name), util.clean_string(dispo), util.clean_string(prix)))

    return results

@exception_safe
def check_materiel(url_list, web_driver):
    output_results = []
    for url in url_list:
        web_driver.get(url)

        nb_resultats = web_driver.find_element_by_xpath('//*[@id="tabProducts"]').text
        nb = util.make_num(nb_resultats)

        results = []
        for i in range(1, int(nb) + 1):
            prix_ = web_driver.find_element_by_xpath(f"//*[@data-position = '{i}']/div[4]/div[1]/span").text[0:-2]
            prix = util.make_num(prix_)
            if(int(prix) >= 850):
                continue

            titre = web_driver.find_element_by_xpath(f"//*[@data-position = '{i}']/div[2]/a/h2").text
            if('water' in titre.lower() or 'hydro' in titre.lower()):
                continue
            
            dispo = web_driver.find_element_by_xpath(f"//*[@data-position = '{i}']/div[3]/div/span[2]").text

            if dispo == 'RUPTURE':
                dispo = "Rupture"

            results.append(('Materiel.net    ' + util.clean_string(titre), util.clean_string(dispo), util.clean_string(prix)))
        
        output_results += results 

    return output_results


