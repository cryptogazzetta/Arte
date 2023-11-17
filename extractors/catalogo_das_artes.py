# External modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
# Project Modules
from utils import csv_handle
from utils import safe_extract_functions
from infra import gcp

## UTILS
def authenticate():
    email = 'gazzetta.art@gmail.com'
    password = 'Senha123'

    login_url = 'https://www.catalogodasartes.com.br/acesso/'
    
    chrome_options = Options()
    chrome_options.binary_location = '/opt/google/chrome'

    # Instantiate ChromeDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(login_url)

    email_field = driver.find_element(By.XPATH, "//input[@id='cliente_email']")
    email_field.send_keys(email)
    password_field = driver.find_element(By.XPATH, "//input[@id='cliente_senha']")
    password_field.send_keys(password)

    enter_button = driver.find_element(By.XPATH, "//button[@class='btn botao-invertido-fixo']")
    enter_button.click()

    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.PARTIAL_LINK_TEXT, "SAIR"))
    finally:
        pass

    return driver

def read_links_and_last_page(links_file_path, links_last_page_file_path):
    try:
        with open(links_file_path, 'r') as f:
            links = list(set(line.strip() for line in f.readlines()))
    except FileNotFoundError:
        links = []
        with open(links_file_path, 'w') as f:
            f.write('')
    try:
        with open(links_last_page_file_path, 'r') as f:
            last_page = int(f.read())
    except FileNotFoundError:
        last_page = 1
        with open(links_last_page_file_path, 'w') as f:
            f.write(str(last_page))

    return links, last_page

def write_links_and_last_page(links_file_path, last_page_file_path, links, last_page):
    with open(links_file_path, 'w') as f:
        f.writelines([link + '\n' for link in links])
    with open(last_page_file_path, 'w') as f:
        f.write(str(last_page))

    gcp.store_file_in_gcs('art_market_data', links_file_path, last_page_file_path)

def remove_link_duplicates():
    with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'r') as f:
        links = f.readlines()
    links = list(set(links))
    with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'w') as f:
        f.writelines(links)


## EXTRACTING LINKS
def get_artworks_links_from_page(driver, base_url, page):
    paintings_url = f'{base_url}{page}/'
    driver.get(paintings_url)
    
    cards = driver.find_elements(By.XPATH, '//div[@class="card-image"]/a')
    return list(set(card.get_attribute('href') for card in cards))

def get_all_artworks_links(base_url, last_page, links_file_path, links_last_page_file_path):
    links, last_page_scraped = read_links_and_last_page(links_file_path, links_last_page_file_path)
    driver = authenticate()

    print(last_page_scraped)

    while last_page_scraped <= last_page:
        new_links = get_artworks_links_from_page(driver, base_url, last_page_scraped)
        new_links = list(set(new_links) - set(links))
        links += new_links
        # Remove duplicates
        links = list(set(links))

        # Write links and last_page_scraped to files
        write_links_and_last_page(links_file_path, links_last_page_file_path, links, last_page_scraped)

        last_page_scraped += 1

    driver.quit()

    return links


## EXTRACTING INFO
def get_artwork_info(driver, link):
    driver.get(link)

    artwork_info = {}
    artwork_info['url'] = link
    # Image URL
    img_url = safe_extract_functions.safe_extract(driver, '//img[contains(@class, "produto-imagem")]')
    if img_url:
        artwork_info['img_url'] = img_url.get_attribute('src')
    # Table content
    try:
        table_element = safe_extract_functions.safe_extract(driver, '//table[@class="produto-tabela"]')
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
    # get links
    with open(links_file_path, 'r') as f:
        artwork_links = f.readlines()
    artwork_links = [link.strip() for link in artwork_links]

    # retrieve 'artworks_info.csv' file if it exists
    try:
        artworks_info = csv_handle.csv_to_dict_list(artworks_info_file_path)
        # remove from artwork_links the URLs already in artworks_info
        artwork_links = [link for link in artwork_links if link not in [artwork_info['url'] for artwork_info in artworks_info]]
        # bring back the ones with 'Error' != False in artworks_info
        artwork_links += [artwork_info['url'] for artwork_info in artworks_info if artwork_info['Error'] != False]
        
    except Exception as e:
        print(e)
        artworks_info = []

    # Check if artwork_links is empty. Otherwise, authenticate and start extracting info
    if not artwork_links:
        print('No new artworks to extract')
        return
    else:
        driver = authenticate()

    new_artworks_info = []
    batch_size = 5

    try:
        for artwork_link in artwork_links[-1600:]:
            print(artwork_link)
            artwork_info = get_artwork_info(driver, artwork_link)
            print(artwork_info)
            new_artworks_info.append(artwork_info)

            if len(new_artworks_info) % batch_size == 0:
                artworks_info += new_artworks_info
                csv_handle.dict_list_to_csv(artworks_info, artworks_info_file_path)

                # if there are at least 2 artworks with value other than False in 'Error', break the loop
                if len([new_artwork_info for new_artwork_info in new_artworks_info if new_artwork_info['Error'] != False]) >= 2:
                    break

                new_artworks_info = []

        if new_artworks_info:
            artworks_info += new_artworks_info
            csv_handle.dict_list_to_csv(artworks_info, artworks_info_file_path)
    except Exception as e:
        print(e)
        pass

    driver.quit()


## DEALING WITH FAILED EXTRACTIONS
def get_failed_artworks_links(info_file_path):
    artworks_info = csv_handle.csv_to_dict_list(info_file_path)
    failed_artworks_links = [artwork_info['url'] for artwork_info in artworks_info]

    return failed_artworks_links
## OBS: pegando de trás pra frente
def get_failed_artworks_info(artworks_info_file_path, failed_artworks_links_file_path):

    failed_artworks_links = get_failed_artworks_links(artworks_info_file_path)
    ## PEGANDO DE TRÁS PRA FRENTE
    failed_artworks_links.reverse()

    with open(failed_artworks_links_file_path, 'w') as f:
        f.writelines([link + '\n' for link in failed_artworks_links])

    print(f'Failed artworks links saved to {failed_artworks_links_file_path}')
    
    get_all_artworks_info(failed_artworks_links_file_path, artworks_info_file_path)

