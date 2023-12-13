# External Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import pandas as pd
# Project Modules
from utils import constants
from extractors import utils


def authenticate(url, click_to_log=False):
    
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    if click_to_log:
        login_button = utils.explicit_wait(driver, '//button[@class="Button__Container-sc-1bhxy1c-0 ittcNr"]')[0]
        login_button.click()

    # Use Explicit Wait for the email field to be visible and interactable
    email_field = utils.explicit_wait(driver, '//input[@name="email"]')[0]
    email_field.send_keys(constants.ARTSY_EMAIL)

    # Use Explicit Wait for the password field to be visible and interactable
    password_field = utils.explicit_wait(driver, '//input[@name="password"]')[0]
    password_field.send_keys(constants.ARTSY_PASSWORD)

    # Use Explicit Wait for the submit button to be clickable
    submit_button = utils.explicit_wait(driver, '//button[@type="submit"]')[0]
    submit_button.click()

    print('Authenticated!')
    return driver


## EXTRACTING LINKS
def get_artworks_links_from_page(driver, base_url, page):
    paintings_url = f'{base_url}{page}/'
    driver.get(paintings_url)

    past_auctions_div = utils.explicit_wait(driver, '//div[contains(text(), "Past Auctions")]')
    # Find all sibling <a> elements of the 'Past Auctions' div
    sibling_a_elements = past_auctions_div.find_elements(By.XPATH, './following-sibling::a')
    # Extract href attributes from the sibling <a> elements
    links = [a.get_attribute('href') for a in sibling_a_elements]

    return links

def get_all_artworks_links_from_artist(artist_name, links_file_path, links_last_page_file_path):
    utils.read_links(links_file_path)
    last_page_scraped = utils.read_last_page(artist_name, links_last_page_file_path)

    base_url = f'https://www.artsy.net/artist/{artist_name}/auction-results?hide_upcoming=false&allow_empty_created_dates=true&currency=&include_estimate_range=false&include_unknown_prices=true&allow_unspecified_sale_dates=true&page='

    driver = authenticate(base_url+str(last_page_scraped), click_to_log=True)

    while True:
        new_links = get_artworks_links_from_page(driver, base_url, last_page_scraped)

        try: # Go to next page
            utils.explicit_wait(driver, '//a[@data-testid="next"]')
            last_page_scraped += 1
        except Exception as e: # To be expected at the last page of results
            logging.exception(e)
            break
        finally:
            utils.write_links(artist_name, new_links, links_file_path)
            utils.write_last_page(links_last_page_file_path, artist_name, last_page_scraped)

    driver.quit()

    return new_links


## EXTRACTING INFO
def get_artwork_info(driver, link):
    driver.get(link)
    print('got to link:', link)

    artwork_info = {}
    artwork_info['url'] = link

    # Dict of info with respective xpath and attribute to be extracted
    info_dict = [{'info': 'img_url', 'xpath': '//div[@data-testid="artwork-lightbox-image"]/img', 'attribute': 'src'},
                 {'info': 'Price', 'xpath': '//div[contains(@class, "Box-sc-15se88d-0 Text-sc-18gcpao-0  bUuBLd")]', 'attribute': 'text'},
                 {'info': 'Price_USD', 'xpath': '//div[contains(@class, "Box-sc-15se88d-0 Text-sc-18gcpao-0 caIGcn egIqXp")]', 'attribute': 'text'},
                 {'info': 'Artist_name', 'xpath': '//a[contains(@class, "RouterLink__RouterAwareLink-sc-1nwbtp5-0 dikvRF")]', 'attribute': 'text'},
                 {'info': 'Artist_url', 'xpath': '//a[contains(@class, "RouterLink__RouterAwareLink-sc-1nwbtp5-0 dikvRF")]', 'attribute': 'href'},
                 {'info': 'Title', 'xpath': '//h1[contains(@class, "Box-sc-15se88d-0 Text-sc-18gcpao-0 OfSrA gyuZDD")]', 'attribute': 'text'},
                 {'info': 'Date', 'xpath': '//div[@class="Box-sc-15se88d-0 Text-sc-18gcpao-0 fIDNCK kFGRHf"]', 'attribute': 'text'}
                ]

    for info_item in info_dict: # Extract info from the artwork page
        try:
            if info_item['attribute'] == 'text':
                info = utils.safe_explicit_wait(driver, info_item['xpath'])[0].text
                artwork_info[info_item['info']] = info.replace('\n', ' ')
            elif info_item['attribute'] == 'src':
                artwork_info[info_item['info']] = utils.explicit_wait(driver, info_item['xpath'])[0].get_attribute('src')
            elif info_item['attribute'] == 'href':
                artwork_info[info_item['info']] = utils.explicit_wait(driver, info_item['xpath'])[0].get_attribute('href')
        except Exception as e:
            print(e)
            artwork_info[info_item['info']] = 'got error extracting info: ' + str(e)
    
    table_rows = utils.explicit_wait(driver, '//div[@class="Box-sc-15se88d-0 giFrDh"]')
    if table_rows: # Extract info from the info table in artwork page
        for row in table_rows:
            key = row.find_element(By.XPATH, './div[1]').text
            value = row.find_element(By.XPATH, './div[2]').text
            artwork_info[key] = value

    return artwork_info

def get_all_artworks_info(links_file_path, artworks_info_file_path):
    # Get artworks links
    artworks_links = utils.read_links(links_file_path)

    # Get existing artworks info
    artworks_info, existing_links = utils.read_artworks_info(artworks_info_file_path)
    artworks_links = list(set(artworks_links) - set(existing_links))
    
    new_artworks_info = pd.DataFrame(columns=['url'])
    batch_size = 50

    driver = authenticate('https://www.artsy.net/auctions', click_to_log=True)

    for artwork_link in artworks_links:
        artwork_info = get_artwork_info(driver, artwork_link)
        new_artworks_info = pd.concat([new_artworks_info, pd.DataFrame([artwork_info])], ignore_index=True)

        if len(new_artworks_info) % batch_size == 0:
            utils.write_artworks_info(artworks_info_file_path, new_artworks_info)
            new_artworks_info = pd.DataFrame(columns=list(artwork_info.keys()))

    if not new_artworks_info.empty:
        utils.write_artworks_info(artworks_info_file_path, new_artworks_info)

    driver.quit()

    return artworks_info
