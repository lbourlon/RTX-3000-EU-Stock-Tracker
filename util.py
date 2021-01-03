import requests
from lxml import html

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


def print_results(results):
    print('')
    [print("=",end='') for i in range(0,56)]
    print(' Result ',end="")
    [print("=",end='') for i in range(0,56)]
    print('')

    if len(results) == 0:
        return

    for titre, dispo, prix in results:
        lim = len(titre)
        if lim > 80:
            lim = 80
        print(f"{titre[0:lim]:<90}{dispo:<20}{prix}€")

    [print("=",end='') for i in range(0,120)]
    print('')


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
        
        except Exception as e:
            print(f" -- Couldn't check stocks will try again later")
            print(f" -- {e}",end="")
            
        return results
    return wrapper