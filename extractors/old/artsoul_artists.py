import requests
from lxml import etree

url = 'https://en.artsoul.com.br/artistas/eliana-amorim'

# get etree
response = requests.get(url)
tree = etree.HTML(response.content)

artist = {}

artist['About'] = tree.xpath('//div[@class="mt-10 !w-full overflow-y-auto px-5 !text-justify text-sm text-gray-500 lg:max-h-64 lg:text-base xl:max-h-[600px] xl:pr-10"]/p/text()')[0]
artist['Galleries'] = tree.xpath('//div[@class="py-10"]/ul/li')