from extractors import catalogo_das_artes
# from preprocessing import catalogo_das_artes
from infra import gcp

# catalogo_das_artes.preprocess('./temporary-files/catalogo_das_artes_artworks_info.csv', './clean-files/catalogo_das_artes_artworks_info.csv')
catalogo_das_artes.remove_info_duplicates('./temporary-files/catalogo_das_artes_artworks_info.csv')

catalogo_das_artes.get_failed_artworks_info('./temporary-files/catalogo_das_artes_artworks_info.csv', './temporary-files/catalogo_das_artes_failed_artworks_links.txt')