# External modules
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# Project Modules
from utils import csv_handle


def authenticate():
    email = 'gazzetta.art@gmail.com'
    password = 'Senha123'

    login_url = 'https://www.catalogodasartes.com.br/acesso/'
    driver = webdriver.Chrome()
    driver.get(login_url)

    email_field = driver.find_element(By.XPATH, "//input[@id='cliente_email']")
    email_field.send_keys(email)
    password_field = driver.find_element(By.XPATH, "//input[@id='cliente_senha']")
    password_field.send_keys(password)

    enter_button = driver.find_element(By.XPATH, "//button[@class='btn botao-invertido-fixo']")
    enter_button.click()
    return driver

def get_all_artworks_links():
    driver = authenticate()
    page = 1
    links = []
    while page <= 13152:
        paintings_url = 'https://www.catalogodasartes.com.br/cotacao/pinturas/ordem/inclusao_mais_recente/pagina/' + str(page) + '/'
        driver.get(paintings_url)

        
        cards = driver.find_elements(By.XPATH, '//div[@class="card-image"]/a')
        try:
            new_links = [card.get_attribute('href') for card in cards]
            links += new_links
        except:
            pass
        page += 1

        if page % 10 == 0:
            with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'w') as f:
                f.writelines([link + '\n' for link in links])

    return links

def get_artwork_info(driver, link):
    driver.get(link)

    html_content_dict = {}

    # get image url
    img_url = safe_extract(driver, '//img[contains(@class, "produto-imagem")]')
    if img_url:
        html_content_dict['img_url'] = img_url.get_attribute('src')

    try:
        # get data from table
        table_element = safe_extract(driver, '//table[@class="produto-tabela"]')
        rows = table_element.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 2:
                key = cells[0].text
                value = cells[1].text
                html_content_dict[key] = value
    except:
        pass

    return html_content_dict

def safe_extract(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.text
    except:
        return None
    
def safe_extract_multiple(driver, xpath):
    try:
        elements = driver.find_elements(By.XPATH, xpath)
        return elements
    except:
        return None


def get_all_artworks_info():
    with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'r') as f:
        artwork_links = f.readlines()
    artwork_links = [link.strip() for link in artwork_links]

    driver = authenticate()

    artworks_info = []
    batch_size = 100
    for artwork_link in artwork_links:
        artwork_info = get_artwork_info(driver, artwork_link)
        artworks_info.append(artwork_info)

        if len(artworks_info) % batch_size == 0:
            csv_handle.dict_list_to_csv(artworks_info, './temporary-files/catalogo_das_artes_artworks_info.csv')
        
    csv_handle.dict_list_to_csv(artworks_info, './temporary-files/catalogo_das_artes_artworks_info.csv')

    driver.quit()