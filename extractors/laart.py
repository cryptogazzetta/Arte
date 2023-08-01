import requests
from lxml import etree
# Project Modules
from infra import gcp
from utils import string_handle

def get_all_artworks_links():    
    current_page_number = 1

    links = []

    while True:
        print(current_page_number)
        url = 'https://laart.art.br/en/works-of-art/page/' + str(current_page_number)

        page = requests.get(url)
        tree = etree.HTML(page.content)

        cards = tree.xpath('//ul[@class="products ul_products products-grid grid-space-default products-grid-3 grid-items xxl-block-grid-5 xl-block-grid-4 lg-block-grid-4 md-block-grid-3 sm-block-grid-2 block-grid-1"]/li')

        for card in cards:
            links.append(card.xpath('.//span[@class="elementor-heading-title elementor-size-default"]/a')[0].get('href'))

        page_numbers = tree.xpath('//ul[@class="page-numbers"]/li/a')
        last_page_number = str(page_numbers[-1].text).strip()
        
        if last_page_number <= str(current_page_number):
            break
        else:
            current_page_number += 1

    links = [link + '\n' for link in links]
    with open('./temporary-files/laart_artworks_links.txt', 'w') as f:
        f.writelines(links)

    gcp.store_file_in_gcs('art_data_files', './temporary-files/laart_artworks_links.txt', 'laart_artworks_links.txt')

    return links



def get_artwork_info(url):
    page = requests.get(url)
    tree = etree.HTML(page.content)

    artwork_info = {}

    artwork_info['Title'] = safe_extract(tree, '//h1[@class="product_title entry-title elementor-heading-title elementor-size-default"]')
    artwork_info['Price'] = safe_extract(tree, '//span[@class="woocommerce-Price-amount amount"]')#[:-2]
    artwork_info['Out of stock'] = safe_extract(tree, '//p[@class="stock out-of-stock"]')
    # artwork_info['Artist'] = 
    # artist_info = tree.xpath('//div[@class="elementor-element elementor-element-1f9400b2 elementor-widget elementor-widget-woocommerce-product-content"]/div/p')

    print(artist_info[0].text)



    # from more_info, get 'Técnica' as string after 'Técnica: '
    # artwork_info['Technique'] = more_info.split('Técnica: ')[1]
    # artwork_info['Dimensions'] = more_info.split('Tamanho: ')[1]

    print(artwork_info)


def safe_extract(tree, xpath, index=0):
    try:
        return tree.xpath(xpath)[index].text
    except:
        return None
    
def safe_extract_attribute(tree, xpath, attribute, index=0):
    try:
        return tree.xpath(xpath)[index].get_attribute(attribute)
    except:
        return None