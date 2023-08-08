from extractors import laart, blombo, galeria22, nano
from infra import gcp
from selenium import webdriver
from analysis import saatchi_prepare_artists


print(nano.get_artwork_info('https://nanoartmarket.com.br/product/alexandre-freire-2/'))