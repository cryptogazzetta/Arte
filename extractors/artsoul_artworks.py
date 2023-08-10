# External modules
from lxml import etree
import requests
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import csv
# Project modules
from infra import gcp
from utils import csv_handle, string_handle


def get_all_artworks_links():

    url = 'https://artsoul.com.br/obras'
    driver = webdriver.Chrome()
    driver.get(url)

    # try:
    #     close_modal_button = driver.find_element(By.XPATH, '//a[@class="absolute p-1 bg-white cursor-pointer group rounded-me top-1 right-1"]')
    #     close_modal_button.click()
    # except:
    #     print('modal not found')
    #     time.sleep(10)
    #     close_modal_button = driver.find_element(By.XPATH, '//a[@class="absolute p-1 bg-white cursor-pointer group rounded-me top-1 right-1"]')
    #     close_modal_button.click()

    # try:
    #     accept_cookies_button = driver.find_element(By.XPATH, '//a[@class="flex items-center justify-center px-4 py-2 text-sm font-medium text-yellow-800 transition bg-yellow-400 cursor-pointer rounded-me js-cookie-consent-agree cookie-consent__agree hover:bg-yellow-300"]')
    #     accept_cookies_button.click()
    # except:
    #     print('cookies button not found')
    #     time.sleep(10)
    #     close_modal_button = driver.find_element(By.XPATH, '//a[@class="absolute p-1 bg-white cursor-pointer group rounded-me top-1 right-1"]')
    #     close_modal_button.click()

    while True:
        load_more_button = driver.find_element(By.XPATH, '//button[@class="flex items-center justify-center w-full h-12 font-semibold text-white transition bg-gray-500 rounded-me mt-14 px-7 hover:bg-gray-600 lg:mx-auto lg:w-auto"]')
        try:
            load_more_button.click()
            time.sleep(5)
        except Exception as e:
            print(e)
            print('load more button not found')
            break
        
    links_object = driver.find_elements(By.XPATH, '//div[@class="w-full relative inline-block"]/div[@class="relative"]/a')
    links = [link.get_attribute('href') for link in links_object]

    driver.quit()

    print(links)
    print(len(links))

    # save links as txt file
    with open('./temporary-files/artsoul_artworks_links.txt', 'w') as f:
        f.writelines([link + '\n' for link in links])

    # upload links to gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/artsoul_artworks_links.txt', 'artsoul_artworks_links.txt')

    return links


def get_artwork_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    artwork_info = {}
    artwork_info['url'] = url

    price = safe_extract_info(soup, 'h2', 'text-3xl text-gray-500')
    if price != None:
        artwork_info['Price'] = string_handle.get_number(price)[:-2]
    artwork_info['Artist'] = safe_extract_info(soup, 'span',  'text-sm font-semibold text-gray-500 transition group-hover:text-cyan-500').replace('\n', '')
    artwork_info['Artist_url'] = safe_extract_info(soup, 'a', 'flex items-center h-8 px-5 text-xs font-semibold text-gray-400 uppercase transition border border-gray-300 rounded-me hover:border-cyan-400 hover:bg-cyan-400 hover:text-white', 'href')
    artwork_info['Title'] = safe_extract_info(soup, 'h1', 'mt-3 mb-5 text-xl font-bold text-gray-500 lg:text-3xl')
    artwork_info['Description'] = safe_extract_info(soup, 'div', 'prose !text-sm !normal-case !text-gray-400')
    location_and_year = soup.find('div', 'flex mt-3 text-sm text-gray-400 lg:mt-0')
    artwork_info['Location'] = safe_extract_multiple_info(location_and_year, 'p', 0)
    artwork_info['Year'] = safe_extract_multiple_info(location_and_year, 'p', 1)

    try:
        gallery = soup.find_all('h3', class_='text-3xl font-semibold text-gray-500 whitespace-pre-line lg:text-4xl')
        #from list, get element that contains 'Mais Obras da Galeria'
        gallery = [g for g in gallery if 'Mais Obras da Galeria' in g.text][0].text
        gallery = gallery.split('Mais Obras da Galeria ')[1].strip()
    except:
        gallery = None
    artwork_info['Gallery'] = gallery

    
    technical_data_sheet_div = soup.find('div', 'flex flex-col space-y-1 text-sm text-gray-400 normal-case')

    measurements_div = technical_data_sheet_div.find('div', 'flex items-center')
    artwork_info['Height'] = safe_extract_multiple_info(measurements_div, 'span', 0, 'px-2')
    artwork_info['Width'] = safe_extract_multiple_info(measurements_div, 'span', 1, 'px-2')
    artwork_info['Depth'] = safe_extract_multiple_info(measurements_div, 'span', 2, 'px-2')

    info_divs = technical_data_sheet_div.find_all('div', {'class': 'flex flex-col lg:flex-row lg:items-center'})
    for div in info_divs:
        info_type = safe_extract_info(div, 'b', '').replace(':', '')
        info = []
        if div.select_one('p span'):
            info = [span.text.strip() for span in div.select('p span')]
        else:
            info = [div.select_one('p').text.strip()]
        artwork_info[info_type] = info

    return artwork_info



def get_all_artworks_info():
    
    artworks_links = gcp.retrieve_file_from_gcs('art_data_files', 'artsoul_artworks_links.txt', './temporary-files/artsoul_artworks_links.txt')
    with open('./temporary-files/artsoul_artworks_links.txt', "r", encoding="utf-8") as file:
        artworks_links = [line.strip() for line in file]

    ## tirar "en." depois de "https://"
    # artworks_links = [link.replace('en.', '') for link in artworks_links]

    artworks_info = []
    failed_artworks_urls = []

    for link in artworks_links:
        try:
            artworks_info.append(get_artwork_info(link))
        except Exception as e:
            print(e)
            failed_artworks_urls.append({'url': link, 'error': str(e)})
            print(f'failed to get artwork info for {link}')


    dict_list_to_csv(artworks_info, './temporary-files/artsoul_artworks_info.csv')
    # failed_artworks_urls to json with json dump
    if failed_artworks_urls:
        with open('./temporary-files/artsoul_failed_artworks_urls.json', 'w') as f:
            f.write(json.dumps(failed_artworks_urls))

    gcp.store_file_in_gcs('art_data_files', './temporary-files/artsoul_artworks_info.csv', 'artsoul_artworks_info.csv')
    gcp.store_file_in_gcs('art_data_files', './temporary-files/artsoul_failed_artworks_urls.json', 'artsoul_failed_artworks_urls.json')

    return artworks_info, failed_artworks_urls


def safe_extract_info(soup, tag, selector, attribute=None):
    try:
        info = soup.find(tag, {'class': selector})
        if info:
            if attribute:
                return info[attribute]
            return info.text.strip().replace('\n', ' ')
    except AttributeError:
        return ""
    
    
def safe_extract_multiple_info(soup, tag, index, selector=None):
    try:
        if selector:
            items = soup.find_all(tag, {'class': selector})
        else:
            items = soup.find_all(tag)
        if items and 0 <= index < len(items):
            return items[index].text.strip()
    except AttributeError:
        return ""


def dict_list_to_csv(dict_list, info_local_file_path):
    # Define the desired order of columns
    fieldnames = [
        'url', 'Price', 'Artist', 'Artist_url', 'Title', 'Description',
        'Height', 'Width', 'Depth', 'Location', 'Year', 'Techniques',
        'Topics', 'Colours', 'Gallery'
    ]

    with open(info_local_file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_list)