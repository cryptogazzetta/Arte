import requests
from lxml import etree

def get_all_artworks_links():
    url = 'https://www.sp-arte.com/obras/'

    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)
    dom = etree.HTML(response.text)

    links = dom.xpath('//div[@class="archive-item-texts"]/a/@href')
    print(links)