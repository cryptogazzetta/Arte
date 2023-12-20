from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import artsy_auctions as artsy_preprocess, catalogo_das_artes as catalogo_preprocess


## CATÁLOGO DAS ARTES
catalogo_links_file_path = './temporary-files/catalogo_artworks_links.csv'
catalogo_links_last_page_file_path = './temporary-files/catalogo_links_last_page.csv'
catalogo_info_file_path = './temporary-files/catalogo_artworks_info.csv'

artists_list = ["Aldemir Martins", "Cicero Dias - Cícero Dias", "Vicente do Rego Monteiro", "Oswaldo Goeldi", "Adriana Varejao", "Beatriz Milhazes", "Francisco Domingos da Silva - Chico da Silva - Francisco da Silva", "Tomie Ohtake", "Nuno Ramos - Nuno Álvares Pessoa de Almeida Ramos", "Alfredo Volpi", "Marepe (1970)", "Jose Leonilson Bezerra Dias - Leonilson - Dito"]

# for artist in artists_list:
#     catalogo_extract.get_all_artworks_links_from_artist(artist, catalogo_links_file_path, catalogo_links_last_page_file_path)
for i in range(1,10):
    catalogo_extract.get_all_artworks_info(catalogo_links_file_path, catalogo_info_file_path)


## ARTSY AUCTIONS
artsy_links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
artsy_links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
artsy_artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'

# artsy_extract.get_all_artworks_info(artsy_links_file_path, artsy_artworks_info_file_path)