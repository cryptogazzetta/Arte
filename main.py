from extractors import artsy_artworks, nano
from infra import gcp

url = 'https://www.artsy.net/artwork/adrian-kay-wong-blue-hour-whats-left-is-for-tomorrow'
artsy_artworks.get_artwork_info(url)
