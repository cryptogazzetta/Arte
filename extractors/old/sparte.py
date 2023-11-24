from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import csv
# Project Modules
from infra import gcp
from utils import string_handle



def get_all_artworks_links():
    url = 'https://www.sp-arte.com/obras/'

    driver = webdriver.Chrome()
    driver.get(url)

    links_len = 0
    while True:
        # scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        # get all links
        links_objects = driver.find_elements(By.XPATH, '//div[@class="archive-item-texts"]//a[@class="no-underline"]')
        # check if len of links changed
        if links_len != len(links_objects):
            links_len = len(links_objects)
        else:
            break
    driver.quit()

    links = [link.get_attribute('href') for link in links_objects]
    # save links as txt file
    with open('./temporary-files/sparte_artworks_links.txt', 'w') as f:
        f.writelines([link + '\n' for link in links])
    # upload links to gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/sparte_artworks_links.txt', 'sparte_artworks_links.txt')
    
    return links


def get_artwork_info(driver):
    artwork_info = {}
    artwork_info['Link'] = driver.current_url
    artwork_info['Title'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-infos"]/h1').split(',')[0]
    artwork_info['Year'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-infos"]/h1').split(',')[-1]
    artwork_info['Artist'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-artist common-links"]/h3/a')
    artwork_info['Description'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-infos"]/h6', 1)
    artwork_info['Size'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-infos"]/h6', 0)
    artwork_info['Price'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-infos"]/h6[@class="price padding-top-1r"]', -1)
    artwork_info['Gallery'] = safe_extract(driver, '//div[@class="vr-artwork-info-block block-gallery common-links"]/h5/a')
    artwork_info['GalleryLink'] = safe_extract_attribute(driver, '//div[@class="vr-artwork-info-block block-gallery common-links"]/h5/a', 'href')
    artwork_info['ArtistLink'] = safe_extract_attribute(driver, '//div[@class="vr-artwork-info-block block-artist common-links"]/h3/a', 'href')

    return artwork_info


def fix_artwork_info(artwork_df):
    artwork_info = artwork_df.copy()

    artwork_info['Width'] = artwork_info['Size'].split('x')[0]
    artwork_info['Width'] = string_handle.get_number(artwork_info['Width'])
    artwork_info['Height'] = artwork_info['Size'].split('x')[1]
    artwork_info['Height'] = string_handle.get_number(artwork_info['Height'])
    artwork_info['Depth'] = artwork_info['Size'].split('x')[2]
    artwork_info['Depth'] = string_handle.get_number(artwork_info['Depth'])
    
    if '-' in artwork_info['Price']:
        artwork_info['Price'] = artwork_info['Price'].split('-')[0]
        artwork_info['MaxPrice'] = artwork_info['Price'].split('-')[1]
    artwork_info['Price'] = string_handle.get_number(artwork_info['Price'])

    return artwork_info


def get_all_artworks_info(bucket_name, gcp_links_file, output_file, failed_urls_file):
    # get links from gcp
    gcp.retrieve_file_from_gcs(bucket_name, gcp_links_file, './temporary-files/' + gcp_links_file)
    # read links from file
    with open('./temporary-files/' + gcp_links_file, 'r') as f:
        links = f.readlines()
    # get artworks info
    artworks_info = []
    failed_urls = []
    driver = webdriver.Chrome()
    for link in links:
        try:
            driver.get(link)
            artworks_info.append(get_artwork_info(driver))
        except:
            failed_urls.append(link)
    driver.quit()
    
    # save artworks_info as csv file
    string_handle.dict_list_to_csv(artworks_info, './temporary-files/' + output_file)
    gcp.store_file_in_gcs(bucket_name, './temporary-files/' + output_file, output_file)
    
    # save failed_urls as json file
    if failed_urls_file:
        with open('./temporary-files/' + failed_urls_file, 'w') as f:
            f.write(json.dumps(failed_urls))
        gcp.store_file_in_gcs(bucket_name, './temporary-files/' + failed_urls_file, failed_urls_file)


def safe_extract(driver, xpath, index=None):
    if index is not None:
        try:
            return string_handle.remove_unicode(driver.find_elements(By.XPATH, xpath)[index].text).replace('\n', ' ')
        except:
            return None
    else:
        try:
            return string_handle.remove_unicode(driver.find_element(By.XPATH, xpath).text).replace('\n', ' ')
        except:
            return None
        
def safe_extract_attribute(driver, xpath, attribute):
    try:
        return driver.find_element(By.XPATH, xpath).get_attribute(attribute).replace('\n', ' ')
    except:
        return None
        


