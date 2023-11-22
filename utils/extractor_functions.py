from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Usage example:
# artsy_extract.get_all_artworks_links('https://www.artsy.net/artist/victor-vasarely/auction-results?hide_upcoming=false&allow_empty_created_dates=true&currency=&include_estimate_range=false&include_unknown_prices=true&allow_unspecified_sale_dates=true&page=', './temporary-files/artsy_auctions_artworks_links.txt', './temporary-files/artsy_auctions_last_page.txt')
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


def explicit_wait(driver, search_key, by='xpath', timeout=10):
    if by == 'xpath':    
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, search_key))
        )
    elif by == 'partial_link_text':
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, search_key))
        )
    elif by == 'tag_name':
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.TAG_NAME, search_key))
        )