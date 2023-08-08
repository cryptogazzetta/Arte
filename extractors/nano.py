# External modules
import requests
from lxml import etree
# Project modules
from infra import gcp

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
    artwork_info['Artist'] = safe_extract(tree, '//h2[@class="product_title entry-title"]')
    

    section = tree.xpath('//section[@class="elementor-section elementor-inner-section elementor-element elementor-element-97b2bbf elementor-section-boxed elementor-section-height-default elementor-section-height-default exad-parallax-effect-no exad-background-color-change-no exad-glass-effect-no exad-sticky-section-no exad-particles-section"]')#[0].text
    print(section)


    return artwork_info

def safe_extract(tree, xpath):
    try:
        return tree.xpath(xpath)[0].text
    except:
        return None