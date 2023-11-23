# External modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
# Project Modules
from utils import csv_handle
from utils import extractor_functions
from infra import gcp


## UTILS
def authenticate():
    email = 'gazzetta.art@gmail.com'
    password = 'Senha123'

    login_url = 'https://www.catalogodasartes.com.br/acesso/'
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.binary_location = '/opt/google/chrome'

    # Instantiate ChromeDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(login_url)

    
    email_field = extractor_functions.explicit_wait(driver, "//input[@id='cliente_email']")
    email_field.send_keys(email)
    password_field = extractor_functions.explicit_wait(driver, "//input[@id='cliente_senha']")
    password_field.send_keys(password)

    enter_button = extractor_functions.explicit_wait(driver, "//button[@class='btn botao-invertido-fixo']")
    enter_button.click()

    try:
        extractor_functions.explicit_wait(driver, "SAIR", by='partial_link_text')
    finally:
        pass

    return driver


## EXTRACTING LINKS
def get_artworks_links_from_page(driver, base_url, page):
    paintings_url = f'{base_url}{page}/'
    driver.get(paintings_url)
    
    cards = extractor_functions.explicit_wait(driver, '//div[@class="card-image"]/a')
    return list(set(card.get_attribute('href') for card in cards))

def get_all_artworks_links(base_url, last_page, links_file_path, links_last_page_file_path):
    links, last_page_scraped = extractor_functions.read_links_and_last_page(links_file_path, links_last_page_file_path)
    print(last_page_scraped)

    driver = authenticate()

    while last_page_scraped <= last_page:
        new_links = get_artworks_links_from_page(driver, base_url, last_page_scraped)
        links += new_links
        # Remove duplicates
        links = list(set(links))

        extractor_functions.write_links_and_last_page(links_file_path, links_last_page_file_path, links, last_page_scraped)
        last_page_scraped += 1

    driver.quit()

    return links

def remove_link_duplicates(links_file_path):
    with open(links_file_path, 'r') as f:
        links = f.readlines()
    links = list(set(links))
    with open(links_file_path, 'w') as f:
        f.writelines(links)


## EXTRACTING INFO
def get_artwork_info(driver, link):
    driver.get(link)

    artwork_info = {}
    artwork_info['url'] = link
    # Image URL
    try:
        artwork_info['img_url'] = extractor_functions.explicit_wait(driver, '//img[contains(@class, "produto-imagem")]').get_attribute('src')
    except:
        artwork_info['img_url'] = None
        
    # Table content
    try:
        table_element = extractor_functions.explicit_wait(driver, '//table[@class="produto-tabela"]')
        rows = table_element.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 2:
                key = cells[0].text
                value = cells[1].text.replace('\n', ' ')
                artwork_info[key] = value

                if key == 'Artista':
                    artwork_info['artist_link'] = cells[1].find_element(By.TAG_NAME, 'a').get_attribute('href')
        artwork_info['Error'] = False
    except Exception as e:
        artwork_info['Error'] = e
        print(e)
        pass
    
    return artwork_info

def get_all_artworks_info(links_file_path, artworks_info_file_path):
    artworks_links = extractor_functions.read_artworks_links_file(links_file_path)
    
    if not artworks_links:
        print('No new artworks to extract')
        return
    else:
        pass

    artworks_info = pd.read_csv(artworks_info_file_path) 
    existing_links = artworks_info['url'].tolist()
    artworks_links = [link for link in artworks_links if link not in existing_links]

    driver = authenticate()

    new_artworks_info = []
    batch_size = 10

    try:
        for artwork_link in artworks_links:
            artwork_info = get_artwork_info(driver, artwork_link)
            new_artworks_info.append(artwork_info)

            if len(new_artworks_info) % batch_size == 0:
                artworks_info = pd.concat([artworks_info, pd.DataFrame(new_artworks_info)])
                artworks_info.to_csv(artworks_info_file_path)

                # if there are at least 2 artworks with value other than False in 'Error', break the loop
                if len([new_artwork_info for new_artwork_info in new_artworks_info if new_artwork_info['Error'] != False]) >= 3:
                    break

                new_artworks_info = []

        if new_artworks_info:
            artworks_info = pd.concat([artworks_info, pd.DataFrame(new_artworks_info)])
            artworks_info.to_csv(artworks_info_file_path)
    except Exception as e:
        print(e)
        pass

    driver.quit()

    remove_info_duplicates(artworks_info_file_path)

    return artworks_info

def remove_info_duplicates(artworks_info_file_path):
    artworks_info = pd.read_csv(artworks_info_file_path)
    artworks_info = artworks_info.sort_values(by=['Error'])
    artworks_info = artworks_info.drop_duplicates(subset=['url'], keep='last')
    artworks_info.to_csv(artworks_info_file_path, index=False)


## DEALING WITH FAILED EXTRACTIONS
def get_failed_artworks_links(artworks_info_file_path):
    artworks_info = csv_handle.csv_to_dict_list(artworks_info_file_path)
    
    failed_artworks_links = [artwork_info['url'] for artwork_info in artworks_info if artwork_info['Error'] != 'False']
    return failed_artworks_links

def get_failed_artworks_info(artworks_info_file_path, failed_artworks_links_file_path):

    failed_artworks_links = get_failed_artworks_links(artworks_info_file_path)
    print('Failed artworks links:' + str(len(failed_artworks_links)))

    with open(failed_artworks_links_file_path, 'w') as f:
        f.writelines([link + '\n' for link in failed_artworks_links])

    print(f'Failed artworks links saved to {failed_artworks_links_file_path}')
    
    artworks_info = get_all_artworks_info(failed_artworks_links_file_path, artworks_info_file_path)

    remove_info_duplicates(artworks_info_file_path)