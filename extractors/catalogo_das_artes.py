# External modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import logging
# Project Modules
from extractors import utils


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

    
    email_field = utils.explicit_wait(driver, "//input[@id='cliente_email']")[0]
    email_field.send_keys(email)
    password_field = utils.explicit_wait(driver, "//input[@id='cliente_senha']")[0]
    password_field.send_keys(password)

    enter_button = utils.explicit_wait(driver, "//button[@class='btn botao-invertido-fixo']")[0]
    enter_button.click()

    try:
        utils.explicit_wait(driver, "SAIR", by='partial_link_text')
    finally:
        pass

    return driver

## EXTRACTING LINKS
def get_artworks_links_from_page(driver, base_url, page):
    paintings_url = f'{base_url}{page}/'
    print(paintings_url)
    driver.get(paintings_url)
    
    cards = utils.explicit_wait(driver, '//div[@class="card-image"]/a')
    links = [card.get_attribute('href') for card in cards]
    links = [link for link in links if link != None]
    return links

def get_all_artworks_links_from_artist(artist_name, links_file_path, links_last_page_file_path):
    utils.read_links(links_file_path)
    last_page_scraped = utils.read_last_page(artist_name, links_last_page_file_path)
    
    base_url = f'https://www.catalogodasartes.com.br/cotacao/pinturas/artista/{artist_name}/ordem/inclusao_mais_recente/pagina/'

    driver = authenticate()

    while True:
        new_links = get_artworks_links_from_page(driver, base_url, last_page_scraped)
        try: # Go to next page
            last_page = utils.explicit_wait(driver, "//div[@class='col s12 m12 l12']/h5")[-1].text.split(' ')[-1]
            if last_page_scraped == int(last_page):
                break
            else:
                last_page_scraped += 1
        except Exception as e: # To be expected at the last page of results
            logging.exception(e)
            break
        finally:
            utils.write_links(artist_name, new_links, links_file_path)
            utils.write_last_page(links_last_page_file_path, artist_name, last_page_scraped)

    driver.quit()

    return new_links

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
        artwork_info['img_url'] = utils.explicit_wait(driver, '//img[contains(@class, "produto-imagem")]')[0].get_attribute('src')
    except:
        artwork_info['img_url'] = None    
    # Table content
    try:
        table_element = utils.explicit_wait(driver, '//table[@class="produto-tabela"]')[0]
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
    artworks_links = utils.read_links(links_file_path)

    artworks_info, existing_links = utils.read_artworks_info(artworks_info_file_path)
    artworks_links = list(set(artworks_links) - set(existing_links))

    new_artworks_info = pd.DataFrame(columns=artworks_info.columns)
    batch_size = 5
    error_tolerance = 2

    driver = authenticate()

    try:
        for artwork_link in artworks_links:
            print(f'going for link: {artwork_link}')
            artwork_info = get_artwork_info(driver, artwork_link)
            artwork_info = pd.DataFrame([artwork_info])

            new_artworks_info = pd.concat([new_artworks_info, artwork_info], ignore_index=True)

            if len(new_artworks_info) % batch_size == 0: # At batch size, write to file
                
                new_artworks_info = new_artworks_info[new_artworks_info['Error'] == False] # Remove errors
                utils.write_artworks_info(artworks_info_file_path, new_artworks_info, lock_path="./temporary-files/lock.txt")

                if (batch_size - len(new_artworks_info)) >= error_tolerance: # Check if error_count >= error_tolerance
                    continue

                new_artworks_info = pd.DataFrame(columns=list(artwork_info.keys())) # Reset new_artworks_info

        if not new_artworks_info.empty: # Write remaining artworks
            utils.write_artworks_info(artworks_info_file_path, new_artworks_info)

    except Exception as e:
        print(e)
    finally:
        driver.quit()

    return artworks_info
