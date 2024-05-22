#from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def generer():

    url = "https://www.safti.fr/trouver-un-conseiller?page=1"
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    nbre_pages = soup.find('a', class_='abtasty-pagination-last-page styles_paginationFirstLast__X4ipW')
    href = nbre_pages.get('href')
    nbre_pages = int(re.search(r'page=(\d+)', href).group(1))

    liens = []
    nombre_de_pages = nbre_pages
    for i in range(nombre_de_pages +1):
        liens.append('https://www.safti.fr/trouver-un-conseiller?page='+str(i))
    liens.pop(0)

    liste_conseillers = []
    liste_villes = []
    liste_telephone = []
    liste_lien_photo = []
    liste_lien_minisite = []

    h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
        }


    for page_url in liens:
        print(f"traitement de la page {liens.index(page_url)+1} sur {len(liens)}")
        response = requests.get(page_url, headers=h)
        if response.status_code != 200:
            print(f"Erreur lors du chargement de la page {page_url} avec le code {response.status_code}.")
            continue  

        soup = BeautifulSoup(response.content, 'html.parser')

        conseillers = soup.find_all('a', attrs={"data-testid": "agent-card-name"})
        villes = soup.find_all('p', class_="saf-p-0 saf-text-[14px] saf-font-medium saf-text-primary")
        telephones = soup.find_all('a', {'data-testid': 'trouverunconseiller-phone-button'})
        images = soup.find_all('img', {'class': 'rounded-circle'})

        # Process each found item
        for i, conseiller in enumerate(conseillers):
            liste_conseillers.append(conseiller.text.strip())
            liste_villes.append(villes[i].text.strip() if i < len(villes) else 'non renseigné')
            liste_lien_photo.append(images[i].get('src', 'non renseigné') if i < len(images) else 'non renseigné')
            liste_lien_minisite.append(conseiller.get('href', 'non renseigné'))        
        
            phone_number = 'non renseigné'  
            if i < len(telephones):
                phone_href = telephones[i].get('href', '')
                if 'tel:' in phone_href:
                    phone_number = phone_href.split('tel:')[-1]
            liste_telephone.append(phone_number)

    base_url = "https://www.safti.fr"
    liste_lien_minisite = [base_url + link if link != 'non renseigné' else 'non renseigné' for link in liste_lien_minisite]

    df = pd.DataFrame({'conseillers' : liste_conseillers, 'telephone' : liste_telephone, 
                    'ville' : liste_villes, 'photo' : liste_lien_photo, 'minisite' : liste_lien_minisite})

    df['telephone'] = df['telephone'].str.replace(' ', '')

    df['ville1'] = df['ville'].str.replace(' et alentours', '')
    df[['ville_nom', 'code_postal']] = df['ville'].str.extract(r'(\D+)\s*\((\d+)\)')
    df.drop('ville', axis=1, inplace=True)
    df.drop('ville1', axis=1, inplace=True)

    df['département'] = df['code_postal'].str.slice(0, 2)

    regions_dict = {
        'Auvergne-Rhône-Alpes': ['01', '03', '07', '15', '26', '38', '42', '43', '63', '69', '73', '74'],
        'Bourgogne-Franche-Comté': ['21', '25', '39', '58', '70', '71', '89', '90'],
        'Bretagne': ['22', '29', '35', '56'],
        'Centre-Val de Loire': ['18', '28', '36', '37', '41', '45'],
        'Corse': ['2A', '2B'],
        'Grand Est': ['08', '10', '51', '52', '54', '55', '57', '67', '68', '88'],
        'Hauts-de-France': ['02', '59', '60', '62', '80'],
        'Île-de-France': ['75', '77', '78', '91', '92', '93', '94', '95'],
        'Normandie': ['14', '27', '50', '61', '76'],
        'Nouvelle-Aquitaine': ['16', '17', '19', '23', '24', '33', '40', '47', '64', '79', '86', '87'],
        'Occitanie': ['09', '11', '12', '30', '31', '32', '34', '46', '48', '65', '66', '81', '82'],
        'Pays de la Loire': ['44', '49', '53', '72', '85'],
        'Provence-Alpes-Côte d\'Azur': ['04', '05', '06', '13', '83', '84'],
        'Corse': ['20'],
        'DOM/TOM': ['97']
    }

    flat_regions_dict = {dept: region for region, depts in regions_dict.items() for dept in depts}

    df['region'] = df['département'].map(flat_regions_dict)

    df.to_csv('contacts_safti_csv.csv')