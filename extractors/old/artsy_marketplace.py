# External Modules
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from lxml import etree
# Project Modules
from infra import gcp
from utils import csv_handle


### GET_ALL_ARTWORKS_LINKS IS SAVING TO DIFFERENT TXT FILE!!! ###


def get_all_artworks_links():
    url = 'https://www.artsy.net/collection/painting?additional_gene_ids%5B0%5D=painting'
    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(2)

    try:
        cookies_consent_button = driver.find_element(By.XPATH, '//button[@class="Button__Container-sc-1bhxy1c-0 bHtEkx"]')
        cookies_consent_button.click()
    except:
        pass

    open_artists_button = driver.find_element(By.XPATH, '//button[@class="Clickable-sc-10cr82y-0 jPuBMs"]')
    open_artists_button.click()
    artists_names_list = driver.find_element(By.XPATH, '//div[@class="Box-sc-15se88d-0 eGPiVT"]').text
    artists_names_list = artists_names_list.split('\n')

    ## TO DO : GET FEATURED ARTISTS LINKS
    
    artworks_links = []
    failed_artists = []
    batch_size = 500

    for artist_name in artists_names_list[2:]:
        try:
            artworks_links += get_artist_artworks_links(driver, artist_name)
        except Exception as e:
            print(e)
            failed_artists.append(artist_name)
            pass

        if len(artworks_links) % batch_size == 0:
            save_artworks_links_txt(artworks_links)
    
    save_artworks_links_txt(artworks_links)

    driver.close()

    return artworks_links


def save_artworks_links_txt(artworks_links):
    with open('./temporary-files/artsy_artworks_links1.txt', 'w') as f:
        f.writelines([link + '\n' for link in artworks_links])


def get_artist_artworks_links(driver, artist_name):
    
    artist_modified_name = artist_name.lower().replace(' ', '-')
    
    artist_artworks_links = []

    page_number = 1
    while True:
        new_url = f'https://www.artsy.net/collection/painting?additional_gene_ids%5B0%5D=painting&artist_ids%5B0%5D={artist_modified_name}&page={page_number}'
        driver.get(new_url)
        artist_artworks_links += [link.get_attribute('href') for link in driver.find_elements(By.XPATH, '//a[@class="RouterLink__RouterAwareLink-sc-1nwbtp5-0 eilryE"]')]

        try:
            next_page_button = driver.find_element(By.XPATH, '//a[@class="Pagination__PageLink-sc-1r2jw01-0 iPdAKY"]')
            page_number += 1
        except:
            break

    return artist_artworks_links


def get_artwork_info(url):
    response = requests.get(url)
    tree = etree.HTML(response.text)
    html = response.text

    artwork_info = {}

    artwork_info['URL'] = url
    artwork_info['Artist'] = extract_safe(tree, '//a[@class="RouterLink__RouterAwareLink-sc-1nwbtp5-0 dikvRF ArtworkSidebarArtists__StyledArtistLink-eqhzb8-0 jdgrPD"]', 0)
    artwork_info['Title'] = extract_safe(tree, '//h1[@class="Box-sc-15se88d-0 Text-sc-18gcpao-0 caIGcn bhlKfb"]/i', 0)
    artwork_info['Price'] = extract_safe(tree, '//div[@class="Box-sc-15se88d-0 Text-sc-18gcpao-0 eXbAnU drBoOI"]', 0)
    artwork_info['Gallery'] = extract_safe(tree, '//a[@class="RouterLink__RouterAwareLink-sc-1nwbtp5-0 dikvRF ArtworkSidebarPartnerInfo__StyledPartnerLink-sc-16oykvq-1 iDqJfT"]', 0)

    artwork_info['Materials'] = extract_safe(tree, '//div[@class="Box-sc-15se88d-0 Text-sc-18gcpao-0  cgchZM"]', 1)
    artwork_info['Dimensions'] = extract_safe(tree, '//div[@class="Box-sc-15se88d-0 Text-sc-18gcpao-0  cgchZM"]', 2)
    artwork_info['Scarcity'] = extract_safe(tree, '//button[@class="Clickable-sc-10cr82y-0 hgPCQf"]', 0)

    return artwork_info


def get_all_artworks_info():
    # read artworks links from file
    with open('./temporary-files/artsy_artworks_links.txt', 'r') as f:
        artworks_links = f.readlines()

    artworks_links = [link.replace('\n', '') for link in artworks_links]

    artworks_info = []

    batch_size = 100

    for link in artworks_links:
        print(link)
        artwork_info = get_artwork_info(link)
        artworks_info.append(artwork_info)

        if len(artworks_info) % batch_size == 0:
            csv_handle.dict_list_to_csv(artworks_info, './temporary-files/artsy_artworks_info.csv')

    csv_handle.dict_list_to_csv(artworks_info, './temporary-files/artsy_artworks_info.csv')

    return artworks_info


def extract_safe(etree, xpath, index=None):
    if index is None:
        try:
            return etree.xpath(xpath).text
        except Exception as e:
            print(e)
            return None
    else:
        try:
            return etree.xpath(xpath)[index].text
        except Exception as e:
            print(e)
            return None

