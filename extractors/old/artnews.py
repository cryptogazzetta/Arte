# External modules
from bs4 import BeautifulSoup
import requests
from collections import defaultdict
from lxml import etree
import json
# Project modules
from infra import gcp
import extractors.string_handle as string_handle

user_agent = {'User-agent': 'Mozilla/5.0'}


def get_all_articles():

    # If artnews_articles_info.json exists in gcp, retrieve it and store it in articles_info
    if gcp.file_exists('art_data_files', 'artnews_articles_info.json'):
        gcp.retrieve_file_from_gcs('art_data_files', 'artnews_articles_info.json', 'artnews_articles_info.json')
        with open('artnews_articles_info.json', 'r', encoding="utf-8") as file:
            existing_articles_info = json.load(file)
        print('articles_info retrieved from gcp')
    else:
        existing_articles_info = []
    
    topics = ['news', 'market', 'reviews', 'artists']
    for topic in topics:
        new_articles_info = get_articles(topic)
        articles_info = existing_articles_info + [article for article in new_articles_info if article not in existing_articles_info]
        articles_info_json = json.dumps(articles_info)
        with open('artnews_articles_info.json', 'w', encoding="utf-8") as file:
            file.write(articles_info_json)
        gcp.store_file_in_gcs('art_data_files', 'artnews_articles_info.json', 'artnews_articles_info.json')
        print(f'artnews_{topic}_articles_info.json stored in gcp')


def get_articles(topic):
    base_url = 'https://www.artnews.com/c/art-news/'+topic+'/page/'
    
    page = 1
    articles_info = []
    while True:
        url = base_url + str(page)
        response = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(response.text, "html.parser")
        article_cards = soup.find_all('div', class_='lrv-a-grid lrv-a-cols3')
        
        for article_card in article_cards:
            try:
                article_info = {}            
                title = article_card.find('a', class_='c-title__link lrv-a-unstyle-link u-color-brand-primary:hover')
                article_info['title'] = string_handle.remove_unicode(title.text)
                article_info['summary'] = article_card.find('p', class_='c-dek  lrv-u-font-weight-light lrv-u-font-size-16 lrv-u-font-size-18@desktop-xl a-hidden@mobile-max lrv-u-margin-a-00')
                article_info['href'] = title.get('href')
                article_info['timestamp'] = string_handle.remove_unicode(article_card.find('time').text)
                article_info['type'] = article_card.find('a', class_='c-span__link u-color-brand-primary-dark:hover').text.strip()
                articles_info.append(article_info)
            except Exception as e:
                print(e)
                print('Error getting article info')

        # Check if it's the last page
        buttons = soup.find_all('span', class_='c-button__inner')
        buttons_text = [button.text.strip() for button in buttons]
        if (page==1 or 'Next' in buttons_text):
            page += 1
        else:
            print('last page')
            break
    
    return articles_info