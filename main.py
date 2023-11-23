from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import catalogo_das_artes as preprocess

## ARTSY AUCTIONS

links_file_path = './temporary-files/artsy_auctions_artworks_links.txt'
links_last_page_file_path = './temporary-files/artsy_auctions_last_page.txt'
artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'
a = artsy_extract.get_all_artworks_info(links_file_path, artworks_info_file_path)
print(a)



## CATALOGO DAS ARTES

# for i in range(5):
#     catalogo_extract.get_all_artworks_info('./temporary-files/catalogo_das_artes_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')
#     preprocess.preprocess('./temporary-files/catalogo_das_artes_artworks_info.csv', './clean-files/catalogo_das_artes_artworks_info.csv')