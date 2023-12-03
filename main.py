from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import artsy_auctions as artsy_preprocess

## ARTSY AUCTIONS

link = 'https://www.artsy.net/auction-result/4370761'
links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'


artists = ['alfredo-volpi', 'djanira', 'almeida-junior', 'leonilson']
for artist in artists:
    artsy_extract.get_all_artworks_links_from_artist(artist, links_file_path, links_last_page_file_path)

artsy_extract.get_all_artworks_info(links_file_path, artworks_info_file_path)