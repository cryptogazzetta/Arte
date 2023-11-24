import requests
from lxml import etree
import csv
# Project Modules
from infra import gcp
from utils import csv_handle


def get_all_artworks_links():
    
    links = []

    current_page_number = 1

    while True:
        print(current_page_number)
        url = 'https://blombo.com/obras/pinturas?limit=72&p=' + str(current_page_number)

        page = requests.get(url)
        tree = etree.HTML(page.content)


        cards = tree.xpath('//a[@class="product-image"]')

        new_links = [card.get('href') for card in cards]
        links += new_links

        # check for li with class 'soulmkt_pager' with an a with text that contains 'Próximo'
        if tree.xpath('//li[@class="soulmkt_pager"]/a[contains(text(), "Próximo")]'):
            current_page_number += 1
        else:
            break

    # save links as txt file
    with open('./temporary-files/blombo_artworks_links.txt', 'w') as f:
        f.writelines([link + '\n' for link in links])
    # upload links to gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/blombo_artworks_links.txt', 'blombo_artworks_links.txt')

    return links


def get_artwork_info(url):

    page = requests.get(url)
    tree = etree.HTML(page.content)

    artwork_info = {}

    artwork_info['Link'] = url
    artwork_info['Title'] = safe_extract(tree, '//span[@class="h6 product-name"]').replace('Título:', '').strip()
    artwork_info['Artist'] = safe_extract(tree, '//div[@class="product-high-attribute]/h1')
    artwork_info['Old Price'] = safe_extract(tree, '//span[contains(@id, "old-price")]')
    artwork_info['Description'] = safe_extract(tree, '//div[@class="block-description w-100 float-left mt-2 mb-2 "]')
    artwork_info['Available'] = safe_extract(tree, '//span[@class="disponivel"]')
    
    price = safe_extract(tree, '//span[contains(@id, "product-price")]')
    if price == '':
        price = safe_extract(tree, '//span[@class="price"]')
    artwork_info['Price'] = price

    info_li_list = tree.xpath('//div[@class="pd-content w-100 float-left mt-0 highlights_additional_information"]/ul/li')
    
    for info_li in info_li_list:
        
        info_name = safe_extract(info_li, './span/strong').replace(':', '').strip()
        if info_name == 'Artista':
            artwork_info['Artist'] = safe_extract(info_li, './span/a').strip()
            artwork_info['ArtistUrl'] = safe_extract_attribute(info_li, './span/a', 'href')
        
        else:
            info_content = etree.tostring(info_li, method='text', encoding='unicode')
            info_content = info_content.replace(info_name+':', '').strip()
            artwork_info[info_name] = info_content

    return artwork_info



def get_all_artworks_info(bucket_name, gcp_links_file, output_file, failed_urls_file):
    
    gcp.retrieve_file_from_gcs(bucket_name, gcp_links_file, './temporary-files/' + gcp_links_file)
    # read links from file
    with open('./temporary-files/' + gcp_links_file, 'r') as f:
        links = f.readlines()
    # get artworks info
    artworks_info = []
    failed_urls = []

    batch_size = 50

    for link in links:
        try:
            artworks_info.append(get_artwork_info(link.strip()))
            if len(artworks_info) % batch_size == 0:
                store_files(artworks_info, failed_urls, output_file, failed_urls_file)
        except:
            failed_urls.append(link.strip())

    if(artworks_info or failed_urls):
        store_files(artworks_info, failed_urls, output_file, failed_urls_file)

    return artworks_info, failed_urls



def safe_extract(tree, xpath, index=0):
    try:
        return tree.xpath(xpath)[index].text.replace('\n', '')
    except Exception as e:
        print(e)
        return None
    
def safe_extract_attribute(tree, xpath, attribute, index=0):
    try:
        return tree.xpath(xpath)[index].get(attribute).replace('\n', '')
    except:
        return None
    

def store_files(artworks_info, failed_urls, output_file, failed_urls_file):
    # save artworks info as csv file
    csv_handle.dict_list_to_csv(artworks_info, './temporary-files/' + output_file)
    # upload artworks info to gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/' + output_file, output_file)

    # save failed urls as txt file
    with open('./temporary-files/' + failed_urls_file, 'w') as f:
        f.writelines([url + '\n' for url in failed_urls])
    # upload failed urls to gcp
    gcp.store_file_in_gcs('art_data_files', './temporary-files/' + failed_urls_file, failed_urls_file)