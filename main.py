from extractors import catalogo_das_artes
from infra import gcp

for i in range(5):
    catalogo_das_artes.get_all_artworks_info('./temporary-files/catalogo_das_artes_regomonteiro_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')