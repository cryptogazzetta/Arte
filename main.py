from extractors import artsy_auctions as artsy_extract, catalogo_das_artes as catalogo_extract
from preprocessing import catalogo_das_artes as preprocess

## ARTSY AUCTIONS

link = 'https://www.artsy.net/auction-result/4370761'
links_file_path = './temporary-files/artsy_auctions_artworks_links.txt'
links_last_page_file_path = './temporary-files/artsy_auctions_last_page.txt'
artworks_info_file_path = './temporary-files/artsy_auctions_artworks_info.csv'

artists_names = ['marc-chagall', 'emiliano-di-cavalcanti', 'vicente-do-rego-monteiro']
for artist_name in artists_names:
    base_url = f'https://www.artsy.net/artist/{artist_name}/auction-results?hide_upcoming=false&allow_empty_created_dates=true&currency=&include_estimate_range=false&include_unknown_prices=true&allow_unspecified_sale_dates=true&page='
    artsy_extract.get_all_artworks_links(base_url, links_file_path, links_last_page_file_path)
    with open(links_last_page_file_path, 'w') as f:
        f.write('1')
    



## CATALOGO DAS ARTES

# for i in range(5):
#     catalogo_extract.get_all_artworks_info('./temporary-files/catalogo_das_artes_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')
#     preprocess.preprocess('./temporary-files/catalogo_das_artes_artworks_info.csv', './clean-files/catalogo_das_artes_artworks_info.csv')