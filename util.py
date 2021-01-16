import requests
from lxml import html

import shutil, sys
from math import floor

ldlc_urls = ["https://www.ldlc.com/recherche/rtx%203060ti/?sort=1"
             "https://www.ldlc.com/recherche/rtx%203070/?sort=1",
             "https://www.ldlc.com/recherche/rtx%203080/?sort=1"]

targeted_urls_ldlc = ["https://www.ldlc.com/fiche/PB00383518.html", ]

nvidia_founders = "https://www.nvidia.com/fr-fr/shop/geforce/?page=1&limit=9&locale=fr-fr&gpu=RTX%203070,RTX%203070%20Ti,RTX%203080,RTX%203080%20Ti,RTX%203060%20Ti&manufacturer=NVIDIA&gpu_filter=RTX%203090~1,RTX%203080~1,RTX%203070~1,RTX%203060%20Ti~1,RTX%202080%20Ti~0,RTX%202080%20SUPER~0,RTX%202080~0,RTX%202070%20SUPER~0,RTX%202070~0,RTX%202060%20SUPER~0,RTX%202060~0,GTX%201660%20Ti~0,GTX%201660%20SUPER~0,GTX%201660~0,GTX%201650%20Ti~0,GTX%201650%20SUPER~0,GTX%201650~0"

materiel_urls = ["https://www.materiel.net/recherche/rtx%203060%20ti/?sort=1/",
                 "https://www.materiel.net/recherche/rtx%203070/?sort=1/",
                 "https://www.materiel.net/recherche/rtx%203080/?sort=1/"]

top_achat_url = ["https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie_puis_mc_est_rtx%252B3060%252Bti.html",
                 "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie_puis_ordre_est_P_puis_sens_est_ASC_puis_mc_est_rtx%252B3070.html",
                 "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie_puis_mc_est_rtx%252B3080.html"]

pc_componentes_urls = ["https://www.pccomponentes.com/buscar/?query=rtx+3060Ti#pg-1&or-search&fm-6",
                       "https://www.pccomponentes.com/buscar/?query=rtx+3060Ti#pg-1&or-search&fm-6",
                       "https://www.pccomponentes.com/buscar/?query=rtx+3070",
                       "https://www.pccomponentes.com/buscar/?query=rtx+3080"]

def make_num(string):

    nb=""
    for l in string:
        if l.isnumeric():
            nb += l
    
    return nb


def order_by_price(result_tuple):
    return sorted(result_tuple, key=lambda price: price[2])

def clean_string(string):
    new_string = ""
    for c in string:
        if (c == '\t' or c == '\n'):
            continue
        new_string += c

    i = 0
    j = len(new_string) - 1
    while i <= len(new_string):
        if(not new_string[i] == ' '):
            break
        i += 1
    
    while j >= 0:
        if(not new_string[j] == ' '):
            break
        j -= 1
    
    return str(new_string[i:j+1])


def get_tree(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)  
    return tree

#returns the width - 2 of the terminal where this is running
def get_terminal_width():
    return shutil.get_terminal_size().columns - 2

def print_results(results):

    width = get_terminal_width()
    head = " Result "

    print('')
    [print("=",end='') for i in range(0,floor((width-len(head))/2))]
    print(head, end="")
    [print("=",end='') for i in range(0,floor((width-len(head))/2))]
    print('')

    if len(results) == 0:
        message = "No cards available for purchasse at this time."
        lim = width - len(message) - 6
        print(f"|| {message}{' ':<{lim}} ||")

    else:
        liste_3060 = []
        liste_3070 = []
        liste_3080 = []
        reste = []

        list_of_lists = [liste_3060, liste_3070, liste_3080, reste]

        for titre, dispo, prix in results:
            if check_repeat(titre, dispo, prix, list_of_lists):
                continue 

            elif "3060" in titre:
                liste_3060.append((titre, dispo, prix))
            elif "3070" in titre:
                liste_3070.append((titre, dispo, prix))
            elif "3080" in titre:
                liste_3080.append((titre, dispo, prix))
            else:
                reste.append((titre,dispo, prix))
        for liste in list_of_lists:
            for titre, dispo, prix in liste:
                lim = len(titre)

                foo = floor(0.8 * width) - len(prix) - 3 
                ba = floor(0.2 * width) - 3
                
                if lim + 3 >= foo:
                    lim = foo - 4

                print(f"|| {titre[0:lim]:<{foo}}{dispo:<{ba}}{prix}€ ||")

    [print("=",end='') for i in range(0,width)]
    print('\n')

def check_repeat(titre, dispo, prix, list_of_lists):
    for liste in list_of_lists:
        if (titre, dispo, prix) in liste:
            return True

    return False

def filter_results(results):
    out = []
    for titre, dispo, prix in results:
        if(dispo.lower() != "rupture"):
            out.append((titre, dispo, prix))

    return out


def exception_safe(store_checking_function):
    def wrapper(*args, **kwargs):
        results = []
        try:
            results = store_checking_function(*args, **kwargs)
        
        except KeyboardInterrupt:
            sys.exit(0)
        
        except Exception as e:
            width = get_terminal_width()

            print(f" -- Couldn't check stocks will try again later")
            message = str(e)[9:]
            if len(message) > width - 4 : 
                message_limit = width - 12
                message = message[0:message_limit] + "... "

            print(f" -- {message}")
            
        return results
    return wrapper