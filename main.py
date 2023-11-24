from extractors import artsy_auctions as artsy_extract

## ARTSY AUCTIONS

link = 'https://www.artsy.net/auction-result/4370761'
links_file_path = './temporary-files/artsy_auctions_artworks_links.csv'
links_last_page_file_path = './temporary-files/artsy_auctions_last_page.csv'
artworks_info_file_path = './temporary-files/OLD_artsy_auctions_artworks_info.csv'

# Links
# artists_names = ['marc-chagall', 'emiliano-di-cavalcanti', 'vicente-do-rego-monteiro']
# for artist_name in artists_names:
#     artsy_extract.get_all_artworks_links_from_artist(artist_name, links_file_path, links_last_page_file_path)
    
# Info
artsy_extract.get_all_artworks_info(links_file_path, artworks_info_file_path)

## CATALOGO DAS ARTES

# for i in range(5):
#     catalogo_extract.get_all_artworks_info('./temporary-files/catalogo_das_artes_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')
#     preprocess.preprocess('./temporary-files/catalogo_das_artes_artworks_info.csv', './clean-files/catalogo_das_artes_artworks_info.csv')