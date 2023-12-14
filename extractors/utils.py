# External Modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time


## LOCK FILE
def is_locked(lock_path):
    with open(lock_path, 'r') as lock_file:
        if lock_file.read() == 'locked':
            return True
        else:
            return False
        
def lock(lock_path):
    lock_file = open(lock_path, 'w')
    lock_file.write('locked')
    lock_file.close()

def unlock(lock_path):
    lock_file = open(lock_path, 'w')
    lock_file.write('unlocked')
    lock_file.close()

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

def explicit_wait(driver, search_key, by='xpath', timeout=2):
    if by == 'xpath':    
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, search_key))
        )
    elif by == 'partial_link_text':
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, search_key))
        )
    elif by == 'tag_name':
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, search_key))
        )

def safe_explicit_wait(driver, search_key, by='xpath', timeout=2):
    try:
        if by == 'xpath':    
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, search_key))
            )
        elif by == 'partial_link_text':
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, search_key))
            )
        elif by == 'tag_name':
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, search_key))
            )
        elif by == 'class_name':
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, search_key))
            )
    except TimeoutException as e:
        print(f'Timeout waiting for element with search_key: {search_key}')
        # Handle the TimeoutException as needed
        return None
    except Exception as e:
        print(f'Error waiting for element with search_key: {search_key}')
        # Handle other exceptions if needed
        return None


## INTERACT WITH LINKS (TXT)
def read_links(links_file_path, artist=None):
    try:
        links_df = pd.read_csv(links_file_path, names=['url', 'Artist'], header=0)
    except:
        print('No links file found')
        links_df = pd.DataFrame(columns=['url', 'Artist'])

    # Filter links based on the provided artist
    if artist:
        filtered_links = links_df[links_df['Artist'] == artist]['url'].tolist()
    else:
        filtered_links = links_df['url'].tolist()

    return filtered_links

def write_links(artist_name, new_links, links_file_path):
    existing_links_df = pd.read_csv(links_file_path, names=['url', 'Artist'])
    new_links_df = pd.DataFrame({'Artist': [artist_name] * len(new_links), 'url': new_links})
    
    links_df = pd.concat([existing_links_df, new_links_df], ignore_index=True)
    links_df.drop_duplicates(inplace=True)
    links_df.to_csv(links_file_path, index=False)


## INTERACT WITH LAST_PAGE (TXT)
def read_last_page(artist_name, links_last_page_file_path):
    try:
        last_page_file = pd.read_csv(links_last_page_file_path, names=['last_page'])
        last_page = last_page_file.loc[artist_name, 'last_page']
    except:
        last_page = 1
        last_page_file = pd.DataFrame(columns=['last_page'], index = [artist_name])
        last_page_file.to_csv
        
    return last_page

def write_last_page(last_page_file_path, artist_name, last_page):
    last_page_file = pd.read_csv(last_page_file_path, index_col=0, names=['last_page'])
    last_page_file.loc[artist_name, 'last_page'] = last_page
    last_page_file.to_csv(last_page_file_path)


## INTERACT WITH ARTWORKS INFO (CSV)
def read_artworks_info(artworks_info_file_path):
    try:
        artworks_info = pd.read_csv(artworks_info_file_path, error_bad_lines=False)
        existing_links = artworks_info['url'].tolist()
    except:
        artworks_info = pd.DataFrame(columns=['url'], index=[0])
        existing_links = []
    
    return artworks_info, existing_links

def write_artworks_info(artworks_info_file_path, new_artworks_info, lock_path):
    while is_locked(lock_path):
        time.sleep(1)
        print('Waiting for lock to be released')

    lock(lock_path)

    try: # try to read existing file
        existing_artworks_info = pd.read_csv(artworks_info_file_path, on_bad_lines='warn')
    except FileNotFoundError:
        # ask for confirmation before creating a new file
        print('File not found. Create new file?')
        confirmation = input('Y/N: ')
        if confirmation == 'Y':
            existing_artworks_info = pd.DataFrame(columns=['url'])

    new_artworks_info = pd.concat([existing_artworks_info, new_artworks_info], ignore_index=True)
    
    new_artworks_to_add = len(new_artworks_info) - len(existing_artworks_info)
    print(f'New artworks to add: {new_artworks_to_add}')
    
    if new_artworks_to_add > 0: # save as csv only if there are new artworks to add
        new_artworks_info.to_csv(artworks_info_file_path, index=False)
        print(f'Done writing {new_artworks_to_add} artworks info to file: {artworks_info_file_path}')
    else:
        print('No new artworks info to write')

    unlock(lock_path)