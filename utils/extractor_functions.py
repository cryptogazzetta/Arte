from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils import csv_handle
# from infra import gcp

## Utils
def safe_extract(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element
    except:
        print('Error extracting element with xpath: ' + xpath)
        return None
    
def safe_extract_multiple(driver, xpath):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return elements
    except:
        print('Error extracting elements with xpath: ' + xpath)
        return None


def explicit_wait(driver, search_key, by='xpath', timeout=10):
    if by == 'xpath':    
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, search_key))
        )
    elif by == 'partial_link_text':
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, search_key))
        )
    elif by == 'tag_name':
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, search_key))
        )

def safe_explicit_wait(driver, search_key, by='xpath', timeout=10):
    try:
        if by == 'xpath':    
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, search_key))
            )
        elif by == 'partial_link_text':
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, search_key))
            )
        elif by == 'tag_name':
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, search_key))
            )
        elif by == 'class_name':
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, search_key))
            )
    except TimeoutException as e:
        print(f'Timeout waiting for element with search_key: {search_key}')
        # Handle the TimeoutException as needed
        return None
    except Exception as e:
        print(f'Error waiting for element with search_key: {search_key}')
        # Handle other exceptions if needed
        return None

## INTERACT WITH LINKS (TXT), LAST_PAGE (TXT) AND INFO (CSV) FILES
def write_links_and_last_page(links_file_path, last_page_file_path, links, last_page):
    with open(links_file_path, 'w') as f:
        f.writelines([link + '\n' for link in links])
    with open(last_page_file_path, 'w') as f:
        f.write(str(last_page))

    # gcp.store_file_in_gcs('art_market_data', links_file_path, last_page_file_path)

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

def read_artworks_links_file(links_file_path):
    with open(links_file_path, 'r') as f:
            artwork_links = f.readlines()
    artwork_links = [link.strip() for link in artwork_links]
    return artwork_links

def read_artworks_info_file(artworks_info_file_path):
# retrieve 'artworks_info.csv' file if it exists
    try:
        artworks_info = csv_handle.csv_to_dict_list(artworks_info_file_path)
        # remove from artwork_links the URLs already in artworks_info
        artworks_links = [link for link in artworks_links if link not in [artwork_info['url'] for artwork_info in artworks_info]]
        # bring back the ones with 'Error' != False in artworks_info
        artworks_links += [artwork_info['url'] for artwork_info in artworks_info if artwork_info['Error'] != False]
    except Exception as e:
        print(e)
        artworks_info = []
    
    return artworks_info
