from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
# from preprocessing import artsy_auctions as artsy_preprocess


## CATÁLOGO DAS ARTES
catalogo_links_file_path = './temporary-files/catalogo_das_artes_artworks_links.csv'
catalogo_links_last_page_file_path = './temporary-files/catalogo_das_artes_last_page.csv'

artists = [
    'José Pancetti - Giuseppe Gianinni Pancetti - Jose Pancetti',
    'Candido Portinari (1903-1962)',
    'Di Cavalcanti (1897-1976)',
    'Alberto Guignard - Alberto da Veiga Guignard',
    'Antônio Bandeira (1922-1967)',
    'Ismael Nery',
    'Tarsila do Amaral',
    'Maria Martins',
    'Maria Leontina Franco Da Costa',
    'Djanira da Motta e Silva',
    'Ibere Camargo - Iberê Camargo',
    'Milton Dacosta',
    'Cildo Meireles (1948)',
    'Helio Oiticica - Hélio Oiticica',
    'Annita Catarina Malfatti - Anita Malfatti - Anita Malfati',
]

for artist in artists:
    catalogo_extract.get_all_artworks_links_from_artist(artist, catalogo_links_file_path, catalogo_links_last_page_file_path)


## ARTSY AUCTIONS
# artsy_links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
# artsy_links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
# artsy_artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'


# artists = [
#     'antonio-bandeira', 'ismael-nery', 'helio-oiticica', 'cildo-meireles',
#     'anita-malfatti', 'tarsila-do-amaral', 'maria-martins', 'maria-leontina',  'djanira',
#     'milton-dacosta', 'ibere-camargo' #'candido-portinari', 'emiliano-di-cavalcanti', 'alberto-da-veiga-guignard', 'cicero-dias', 'jose-pancetti',
# ]

# for artist in artists:
#     artsy_extract.get_all_artworks_links_from_artist(artist, links_file_path, links_last_page_file_path)