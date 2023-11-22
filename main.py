from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import catalogo_das_artes as preprocess


# for i in range(5):
#     catalogo_extract.get_all_artworks_info('./temporary-files/catalogo_das_artes_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')
#     preprocess.preprocess('./temporary-files/catalogo_das_artes_artworks_info.csv', './clean-files/catalogo_das_artes_artworks_info.csv')

artsy_extract.get_all_artworks_info()