from extractors import artsoul_artworks, saatchi_artworks, saatchi_artists, artnews, artsy, artrio#, sparte
from infra import gcp
from selenium import webdriver
from analysis import saatchi_prepare_artists

# saatchi_artworks.get_all_artworks_info('art_data_files', 'saatchi_artworks_links.txt', 'saatchi_artworks_info1.csv', 'saatchi_failed_artworks_urls.json')

# saatchi_artists.get_all_artists_info('art_data_files', 'saatchi_artists_info.json', 'saatchi_artworks_info.csv')

# saatchi_prepare_artists.prepare_artists_df()

# links = ['https://en.artsoul.com.br/obras/sem-titulo-2239',
#          'https://en.artsoul.com.br/obras/flor-urbana']

# for link in links:
#     print(artsoul_artworks.get_artwork_info(link))

# sparte.get_all_artworks_links()

artsoul_artworks.get_all_artworks_info()