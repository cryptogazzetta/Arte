from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import artsy_auctions as artsy_preprocess, catalogo_das_artes as catalogo_preprocess


## CATÁLOGO DAS ARTES
catalogo_links_file_path = './temporary-files/catalogo_artworks_links.csv'
catalogo_links_last_page_file_path = './temporary-files/catalogo_links_last_page.csv'
catalogo_info_file_path = './temporary-files/catalogo_artworks_info.csv'
catalogo_clean_info_file_path = './clean-files/catalogo_artworks_info.csv'


artists_list = ["Aldemir Martins", "Cicero Dias - Cícero Dias", "Vicente do Rego Monteiro", "Oswaldo Goeldi", "Adriana Varejao", "Beatriz Milhazes", "Francisco Domingos da Silva - Chico da Silva - Francisco da Silva", "Tomie Ohtake", "Nuno Ramos - Nuno Álvares Pessoa de Almeida Ramos", "Alfredo Volpi", "Marepe (1970)", "Jose Leonilson Bezerra Dias - Leonilson - Dito", 'José Pancetti - Giuseppe Gianinni Pancetti - Jose Pancetti', 'Candido Portinari (1903-1962)', 'Di Cavalcanti (1897-1976)', 'Alberto Guignard - Alberto da Veiga Guignard', 'Antônio Bandeira (1922-1967)', 'Ismael Nery', 'Tarsila do Amaral', 'Maria Martins', 'Maria Leontina Franco Da Costa', 'Djanira da Motta e Silva', 'Ibere Camargo - Iberê Camargo', 'Milton Dacosta', 'Cildo Meireles (1948)', 'Helio Oiticica - Hélio Oiticica', 'Annita Catarina Malfatti - Anita Malfatti - Anita Malfati']
# for i in range(1, 100):
#     try:
#         for artist in artists_list:
#             catalogo_extract.get_all_artworks_links_from_artist(artist, catalogo_links_file_path, catalogo_links_last_page_file_path)
#     except:
#         continue

# catalogo_preprocess.preprocess(catalogo_info_file_path, catalogo_clean_info_file_path)

i = 0
while i < 10:
    catalogo_extract.get_all_artworks_info(catalogo_links_file_path, catalogo_info_file_path)
    i += 1


## ARTSY AUCTIONS
artsy_links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
artsy_links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
artsy_artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'

# artsy_extract.get_all_artworks_info(artsy_links_file_path, artsy_artworks_info_file_path)