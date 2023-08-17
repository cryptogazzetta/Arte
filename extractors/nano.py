# External modules
import requests
from lxml import etree
# Project modules
from infra import gcp
from utils import csv_handle


def get_all_artworks_links():
    page = 1
    links = []
    while True:
        print('Page: ', page)
        url = 'https://nanoartmarket.com.br/loja/page/'+str(page)
        response = requests.get(url)
        tree = etree.HTML(response.text)

        links += tree.xpath('//h2[@class="product-title"]/a/@href')

        if not tree.xpath('//a[@class="next page-numbers"]/@href'):
            break
        page += 1
        print('found button: ')

    # save links
    with open('./temporary-files/nano_artworks_links.txt', 'w') as f:
        for link in links:
            f.write(link+'\n')

    # save on gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/nano_artworks_links.txt', 'nano_artworks_links.txt')

    return links


def get_artwork_info(url):
    response = requests.get(url)
    tree = etree.HTML(response.text)

    artwork_info = {}
    artwork_info['URL'] = url
    artwork_info['Artist'] = safe_extract(tree, '//h2[@class="product_title entry-title"]')
    artwork_info['Price'] = tree.xpath('//p[@class="price"]/span/bdi/span/following-sibling::text()')[0]
    artwork_info['Categories'] = safe_extract_from_children(tree, '//*[contains(@id, "product")]/div/div/section[2]/div/div[2]/div/section[2]/div/div[1]/div/div[1]/div/div/div/span').replace('Categorias: ', '')

    sections = tree.xpath('//div[div/h2[contains(text(), "Informações")]]/following-sibling::section')

    for section in sections:
        try:
            info_name = safe_extract(section, './/div/div/div/div/div/p')
            info_content = safe_extract_from_children(section, './/div/div[2]/div/div/div/p')
        except Exception as e:
            print(e)
            info_content = None
        if info_name != 'None':
                artwork_info[info_name] = info_content

    return artwork_info


def get_all_artworks_info():
    gcp.retrieve_file_from_gcs('art_market_data', 'nano_artworks_links.txt', './temporary-files/nano_artworks_links.txt')
    with open('./temporary-files/nano_artworks_links.txt', 'r') as f:
        artworks_links = f.readlines()
    
    artworks_info = []

    for artwork_link in artworks_links:
        artwork_link = artwork_link.strip()
        artwork_info = get_artwork_info(artwork_link)
        artworks_info.append(artwork_info)

    csv_handle.dict_list_to_csv(artworks_info, './temporary-files/nano_artworks_info.csv')
    # save on gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/nano_artworks_info.csv', 'nano_artworks_info.csv')

    return artworks_info


def safe_extract(tree, xpath):
    try:
        return tree.xpath(xpath)[0].text
    except Exception as e:
        print(e)
        return None


def safe_extract_from_children(tree, xpath):    
    try:
        info_p_elements = tree.xpath(xpath)
        for info_p_element in info_p_elements:
            info_content = ''.join(info_p_element.itertext()).strip()
        return info_content

    except Exception as e:
        print(e)
        return None