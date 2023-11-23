# External Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Project Modules
from utils import constants, extractor_functions, csv_handle


## UTILS
def authenticate(url, click_to_log=False):
    
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    if click_to_log:
        login_button = extractor_functions.explicit_wait(driver, '//button[@class="Button__Container-sc-1bhxy1c-0 ittcNr"]')
        login_button.click()

    # Use Explicit Wait for the email field to be visible and interactable
    email_field = extractor_functions.explicit_wait(driver, '//input[@name="email"]')
    email_field.send_keys(constants.ARTSY_EMAIL)

    # Use Explicit Wait for the password field to be visible and interactable
    password_field = extractor_functions.explicit_wait(driver, '//input[@name="password"]')
    password_field.send_keys(constants.ARTSY_PASSWORD)

    # Use Explicit Wait for the submit button to be clickable
    submit_button = extractor_functions.explicit_wait(driver, '//button[@type="submit"]')
    submit_button.click()

    print('Authenticated!')
    return driver

def get_artist_base_url_from_name(artist_name):
    return f'https://www.artsy.net/artist/{artist_name}/auction-results?hide_upcoming=false&allow_empty_created_dates=true&currency=&include_estimate_range=false&include_unknown_prices=true&allow_unspecified_sale_dates=true&page='


## EXTRACTING LINKS
def get_artworks_links_from_page(driver, base_url, page):
    paintings_url = f'{base_url}{page}/'
    driver.get(paintings_url)

    past_auctions_div = extractor_functions.explicit_wait(driver, '//div[contains(text(), "Past Auctions")]')
    # Find all sibling <a> elements of the 'Past Auctions' div
    sibling_a_elements = past_auctions_div.find_elements(By.XPATH, './following-sibling::a')
    # Extract href attributes from the sibling <a> elements
    links = [a.get_attribute('href') for a in sibling_a_elements]

    return links

def get_all_artworks_links(base_url, links_file_path, links_last_page_file_path):
    links, last_page_scraped = extractor_functions.read_links_and_last_page(links_file_path, links_last_page_file_path)
    
    driver = authenticate(base_url+str(last_page_scraped), click_to_log=True)

    while True:
        new_links = get_artworks_links_from_page(driver, base_url, last_page_scraped)
        links += new_links
        # Remove duplicates
        links = list(set(links))

        try:
            extractor_functions.explicit_wait(driver, '//a[@data-testid="next"]')
            last_page_scraped += 1
        except Exception as e:
            print(e)
            break
        finally:
            extractor_functions.write_links_and_last_page(links_file_path, links_last_page_file_path, links, last_page_scraped)

    driver.quit()

    return links


## EXTRACTING INFO
def get_artwork_info(driver, link):
    driver.get(link)
    print('got to link:', link)

    artwork_info = {}
    artwork_info['url'] = link

    artwork_info['Price'] = extractor_functions.safe_explicit_wait(driver, '//div[contains(@class, "Box-sc-15se88d-0 Text-sc-18gcpao-0  bUuBLd")]').text

    # artist = extractor_functions.safe_explicit_wait(driver, '//div[contains(@class, "RouterLink__RouterAwareLink-sc-1nwbtp5-0 dikvRF")]')
    # artwork_info['Artist_name'] = artist.text
    # artwork_info['Artist_url'] = artist.get_attribute('href')
    
    # table_rows = extractor_functions.safe_explicit_wait( '//div[contains(@class, "Box-sc-15se88d-0 giFrDh")]')

    # if table_rows:
    #     for row in table_rows:
    #         key = row.find_element(By.XPATH, './div[1]').text
    #         value = row.find_element(By.XPATH, './div[2]').text
    #         artwork_info[key] = value
        
    return artwork_info

def get_all_artworks_info(links_file_path, artworks_info_file_path):
    # Get artworks links
    artworks_links = extractor_functions.read_artworks_links_file(links_file_path)
    if not artworks_links:
        print('No new artworks to extract')
        return
    else:
        pass
    print('got artworks links')

    # Get existing artworks info
    artworks_info = extractor_functions.read_artworks_info_file(artworks_info_file_path) 
    print('got artworks info')

    driver = authenticate('https://www.artsy.net/auctions', click_to_log=True)

    new_artworks_info = []
    batch_size = 10

    try:
        for artwork_link in artworks_links[:28]:
            artwork_info = get_artwork_info(driver, artwork_link)
            new_artworks_info.append(artwork_info)


            if len(new_artworks_info) % batch_size == 0:
                artworks_info += new_artworks_info
                print('writing to csv')
                csv_handle.dict_list_to_csv(artworks_info, artworks_info_file_path)

                # if there are at least 2 artworks with value other than False in 'Error', break the loop
                if len([new_artwork_info for new_artwork_info in new_artworks_info if new_artwork_info['Error'] != False]) >= 3:
                    break

                new_artworks_info = []

        if new_artworks_info:
            artworks_info += new_artworks_info
            print('writing to csv')
            csv_handle.dict_list_to_csv(artworks_info, artworks_info_file_path)
    except Exception as e:
        print(e)
        pass

    driver.quit()

    return artworks_info