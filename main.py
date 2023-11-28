from extractors import artsy_auctions as artsy_extract
from preprocessing import artsy_auctions as artsy_preprocess

## ARTSY AUCTIONS

link = 'https://www.artsy.net/auction-result/4370761'
links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'

# Extract Links
# artists_names = ['victor-vasarely']
# for artist_name in artists_names:
#     artsy_extract.get_all_artworks_links_from_artist(artist_name, links_file_path, links_last_page_file_path)
    
# Extract Info
artsy_extract.get_all_artworks_info(links_file_path, artworks_info_file_path)

# Preprocess Info
# artsy_preprocess.preprocess(artworks_info_file_path, './clean-files/artsy_auctions_artworks_info.csv')


## CATALOGO DAS ARTES

# for i in range(5):
#     catalogo_extract.get_all_artworks_info('./temporary-files/catalogo_das_artes_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')
#     preprocess.preprocess('./temporary-files/catalogo_das_artes_artworks_info.csv', './clean-files/catalogo_das_artes_artworks_info.csv')