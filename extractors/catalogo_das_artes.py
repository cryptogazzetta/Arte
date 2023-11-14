# External modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# Project Modules
from utils import csv_handle
from utils import safe_extract_functions


def authenticate():
    email = 'gazzetta.art@gmail.com'
    password = 'Senha123'

    login_url = 'https://www.catalogodasartes.com.br/acesso/'
    
    chrome_options = Options()
    chrome_options.binary_location = '/opt/google/chrome'

    # Instantiate ChromeDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(login_url)

    email_field = driver.find_element(By.XPATH, "//input[@id='cliente_email']")
    email_field.send_keys(email)
    password_field = driver.find_element(By.XPATH, "//input[@id='cliente_senha']")
    password_field.send_keys(password)

    enter_button = driver.find_element(By.XPATH, "//button[@class='btn botao-invertido-fixo']")
    enter_button.click()

    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.PARTIAL_LINK_TEXT, "SAIR"))
    finally:
        pass

    return driver


def get_all_artworks_links():
    try:
        # retrieve 'catalogo_das_artes_artworks_links.txt' file if it exists
        with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'r') as f:
            links = f.readlines()
        links = [link.strip() for link in links]
    except:
        # otherwise, create an empty list and txt file
        with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'w') as f:
            pass
        links = []
    
    driver = authenticate()
    page = 1

    links = []
    while page <= 13158:
        paintings_url = 'https://www.catalogodasartes.com.br/cotacao/pinturas/ordem/inclusao_mais_antiga/pagina/' + str(page) + '/'
        driver.get(paintings_url)
        
        cards = driver.find_elements(By.XPATH, '//div[@class="card-image"]/a')
        try:
            new_links = [card.get_attribute('href') for card in cards]
        except:
            pass
        page += 1

        links += new_links
        links = list(set(links))
        if page % 10 == 0:
            with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'w') as f:
                f.writelines([link + '\n' for link in links])

    return links


def get_artwork_info(driver, link):
    driver.get(link)
    artwork_info = {}
    artwork_info['url'] = link
    
    img_url = safe_extract_functions.safe_extract(driver, '//img[contains(@class, "produto-imagem")]')
    if img_url:
        artwork_info['img_url'] = img_url.get_attribute('src')

    try:
        table_element = safe_extract_functions.safe_extract(driver, '//table[@class="produto-tabela"]')
        rows = table_element.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) >= 2:
                key = cells[0].text
                value = cells[1].text
                # ignore new line characters
                value = value.replace('\n', ' ')
                artwork_info[key] = value
        artwork_info['Failed'] = False
    except Exception as e:
        artwork_info['Failed'] = True
        print(e)
        pass
    
    return artwork_info


def get_all_artworks_info():
    with open('./temporary-files/catalogo_das_artes_artworks_links.txt', 'r') as f:
        artwork_links = f.readlines()
    artwork_links = [link.strip() for link in artwork_links]

    driver = authenticate()

    artworks_info = []
    batch_size = 10
    for artwork_link in artwork_links:
        artwork_info = get_artwork_info(driver, artwork_link)
        artworks_info.append(artwork_info)

        if len(artworks_info) % batch_size == 0:
            csv_handle.dict_list_to_csv(artworks_info, './temporary-files/catalogo_das_artes_artworks_info.csv')
        
    csv_handle.dict_list_to_csv(artworks_info, './temporary-files/catalogo_das_artes_artworks_info.csv')

    driver.quit()