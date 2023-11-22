# External Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Project Modules
from utils import constants, extractor_functions


## UTILS
def authenticate(url='https://www.artsy.net/auctions'):
    
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)

    # Use Explicit Wait for the email field to be visible and interactable
    email_field = extractor_functions.explicit_wait(driver, '//input[@name="email"]')
    email_field.send_keys(constants.ARTSY_EMAIL)

    # Use Explicit Wait for the password field to be visible and interactable
    password_field = extractor_functions.explicit_wait(driver, '//input[@name="password"]')
    password_field.send_keys(constants.ARTSY_PASSWORD)

    # Use Explicit Wait for the submit button to be clickable
    submit_button = extractor_functions.explicit_wait(driver, '//button[@type="submit"]')
    submit_button.click()

    return driver


## EXTRACTING LINKS
def get_artworks_links_from_page(driver, base_url, page):
    url = f'{base_url}{page}/'
    driver.get(url)

    past_auctions_div = extractor_functions.explicit_wait(driver, '//div[contains(text(), "Past Auctions")]')
    # Find all sibling <a> elements of the 'Past Auctions' div
    sibling_a_elements = past_auctions_div.find_elements(By.XPATH, './following-sibling::a')
    # Extract href attributes from the sibling <a> elements
    links = [a.get_attribute('href') for a in sibling_a_elements]

    return links

def get_all_artworks_links(base_url, links_file_path, links_last_page_file_path):
    links, last_page_scraped = extractor_functions.read_links_and_last_page(links_file_path, links_last_page_file_path)
    
    driver = webdriver.Chrome()
    driver.get(base_url+str(last_page_scraped))

    login_button = extractor_functions.explicit_wait(driver, '//button[@class="Button__Container-sc-1bhxy1c-0 ittcNr"]')
    login_button.click()
    driver = authenticate()

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

    artwork_info = {}
    artwork_info['url'] = link

    # divs = extractor_functions.explicit_wait(driver, '//div[@class="Box-sc-15se88d-0 GridColumns__Cell-sc-1g9p6xx-1  kkTyCy"]/div/div')
    WebDriverWait(driver, 3)
    divs = driver.find_element(By.XPATH, '//div/div[@class="Box-sc-15se88d-0 Text-sc-18gcpao-0 cXRdiF hOupNU"]')
    # for div in divs:
    #     print('aaaa', div.text)
        
    return divs


def get_all_artworks_info():
    link = 'https://www.artsy.net/auction-result/2272498'
    
    driver = authenticate(link)
    WebDriverWait(driver, 3)
    # driver.get(link)

    artwork_info = get_artwork_info(driver, link)
    print(artwork_info)