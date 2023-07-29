import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from lxml import etree
import json
# Project modules
from extractors import string_handle
from infra import gcp


def get_all_artworks_links():
    url = 'https://artrio.com/marketplace/works'
    driver = webdriver.Chrome()
    driver.get(url)

    # Scroll down to load more elements
    scroll_pause_time = 5  # Adjust as needed
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wait for the page to fully load
    time.sleep(5)

    elems = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="work-item-template mb-40"]/a')))
    
    links = [elem.get_attribute('href') for elem in elems]

    driver.quit()

    with open('artrio_artworks_links.txt', 'w') as f:
        f.writelines([link + '\n' for link in links])

    # upload to GCP
    gcp.upload_file_to_gcp('artrio_artworks_links.txt', 'art_data_files', 'artrio_artworks_links.txt')

    return links



def get_artwork_info(url):
    result = requests.get(url)
    dom = etree.HTML(result.text)     

    artwork_info = {}
    artwork_info['Artist'] = dom.xpath('//div[@class="pl-20"]/h3/a/text()')[0]
    artwork_info['Title'] = string_handle.remove_unicode(dom.xpath('//div[@class="pl-20"]/h3/small/i/text()')[0])
    artwork_info['Size'] = string_handle.remove_unicode(dom.xpath('//div[@class="pl-20"]/small/text()')[0])
    artwork_info['Price'] = string_handle.remove_unicode(dom.xpath('//div[@class="pl-20"]/h3[2]/text()')[0])

    about_artworks_section_xpath = '//div[@class="col-sm-8 col-xs-12"]/div[@class="pt-20 mt-20"]/div[@class="row"]'
    about_artwork_sections = dom.xpath(about_artworks_section_xpath)

    for section in about_artwork_sections:
        try:
            section_name = section.xpath('./div[@class="col-sm-4"]/h4/text()')[0]
        except Exception as e:
            print(e)
            break
        
        try:
            section_content = section.xpath('./div[@class="col-sm-8"]/p/text()')
        except Exception as e:
            section_content = dom.xpath(about_artworks_section_xpath+'/div[@class="col-sm-8"]/div[@class="description"]/p/text()')
        section_content = ' '.join(section_content)
        section_content = string_handle.remove_unicode(section_content)

        artwork_info[section_name] = section_content

    return artwork_info



def get_all_artworks_info():
    # Get all artworks links
    artworks_links_file = get_all_artworks_links()
    artworks_links = [link.strip() for link in artworks_links]

    # Get artworks info
    artworks_info = []
    for link in artworks_links[1:]:
        print(link)
        try:
            artwork_info = get_artwork_info(link)
            artworks_info.append(artwork_info)
        except Exception as e:
            print(e)
            continue

    # Save artworks info as json file
    file_path = 'temporary-files/artrio_artworks_info.json'
    with open(file_path, 'w') as f:
        json.dump(artworks_info, f, indent=4)

    # Upload artworks info to GCP
    gcp.upload_file_to_gcp(file_path, 'art_data_files', 'artrio_artworks_info.json')