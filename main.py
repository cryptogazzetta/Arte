from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import artsy_auctions as artsy_preprocess, catalogo_das_artes as catalogo_preprocess


## CATÁLOGO DAS ARTES
catalogo_links_file_path = './temporary-files/catalogo_artworks_links.csv'
catalogo_links_last_page_file_path = './temporary-files/catalogo_links_last_page.csv'
catalogo_info_file_path = './temporary-files/catalogo_artworks_info.csv'

for i in range(10):
    catalogo_extract.get_all_artworks_info(catalogo_links_file_path, catalogo_info_file_path)
# catalogo_preprocess.preprocess(catalogo_info_file_path, './clean-files/catalogo_artworks_info.csv')

## ARTSY AUCTIONS
artsy_links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
artsy_links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
artsy_artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'

# artsy_extract.get_all_artworks_info(artsy_links_file_path, artsy_artworks_info_file_path)