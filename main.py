from extractors import catalogo_das_artes
from infra import gcp

for i in range(10):
    catalogo_das_artes.get_all_artworks_info('./temporary-files/catalogo_das_artes_artworks_links.txt', './temporary-files/catalogo_das_artes_artworks_info.csv')

# link to all Portinari links
# 'https://www.catalogodasartes.com.br/cotacao/obrasdearte/artista/Candido%20Portinari%20(1903-1962)/ordem/avaliacao_mais_antiga/pagina/'