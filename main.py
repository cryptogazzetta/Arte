from extractors import artsoul_artworks, saatchi_artworks, saatchi_artists, artnews, artsy, artrio, sparte
from infra import gcp
from selenium import webdriver
from analysis import saatchi_prepare_artists


print(sparte.get_all_artworks_info('art_data_files', 'sparte_artworks_links.txt', 'sparte_artworks_info.csv', 'sparte_failed_artworks_urls.json'))