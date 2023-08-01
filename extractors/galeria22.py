from selenium import webdriver
from selenium.webdriver.common.by import By
# Project Modules
from infra import gcp
from utils import csv_handle


def get_all_artworks_links():
    driver = webdriver.Chrome()

    current_page_number = 1

    links = []


    while True:
        print(current_page_number)
        url = 'https://galeria22.com.br/catalogo/?product-page=' + str(current_page_number)
        driver.get(url)

        cards = driver.find_elements(By.XPATH, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')
        for card in cards:
            links.append(card.get_attribute('href'))
        
        try:
            next_page_button = driver.find_element(By.XPATH, '//a[@class="next page-numbers"]')
            current_page_number += 1
        except:
            break
    
    driver.quit()

    with open('./temporary-files/galeria22_artworks_links.txt', 'w') as f:
        f.writelines([link + '\n' for link in links])
    gcp.store_file_in_gcs('art_data_files', './temporary-files/galeria22_artworks_links.txt', 'galeria22_artworks_links.txt')
    
    return links



def get_artwork_info(url):

    driver = webdriver.Chrome()
    driver.get(url)

    artwork_info = {}

    artwork_info['URL'] = url
    artwork_info['Price'] = safe_extract(driver, '//span[@class="woocommerce-Price-amount amount"]/bdi')
    artwork_info['Title'] = safe_extract(driver, '//h1[@class="product_title entry-title"]').split(' (')[0]
    
    artwork_info['Artist'] = safe_extract(driver, '//div[@class="woocommerce-product-details__short-description"]/p', 0).split(' (')[0]
    artwork_info['Dimensions'] = safe_extract(driver, '//div[@class="woocommerce-product-details__short-description"]/p', 2)
    artwork_info['Techniques'] = safe_extract(driver, '//div[@class="woocommerce-product-details__short-description"]/p', 3)	

    return artwork_info


def get_all_artworks_info():
    links = gcp.retrieve_file_from_gcs('art_data_files', 'galeria22_artworks_links.txt', './temporary-files/galeria22_artworks_links.txt').split('\n')
    links = [link for link in links if link != '']
    
    artworks_info = []
    failed_links = []

    batch_size = 3
    
    for link in links[:10]:
        try:
            artworks_info.append(get_artwork_info(link))
            if len(artworks_info) % batch_size == 0:
                store_files('galeria22_artworks_info.csv', artworks_info, failed_links)
        except:
            failed_links.append(link)

    store_files('galeria22_artworks_info.csv', artworks_info, failed_links)
    
    return artworks_info


def store_files(filename, artworks_info, failed_links):
    csv_handle.dict_list_to_csv(artworks_info, './temporary-files/' + filename)
    gcp.store_file_in_gcs('art_data_files', './temporary-files/' + filename, filename)
    with open('./temporary-files/galeria22_failed_links.txt', 'w') as f:
        f.writelines([link + '\n' for link in failed_links])
    gcp.store_file_in_gcs('art_data_files', './temporary-files/galeria22_failed_links.txt', 'galeria22_failed_links.txt')

def safe_extract(driver, xpath, index=None):
    if index is None:
        try:
            return driver.find_element(By.XPATH, xpath).text.replace('\n', ' ')
        except:
            return None
    else:
        try:
            return driver.find_elements(By.XPATH, xpath)[index].text.replace('\n', ' ')
        except:
            return None
    