# from extractors import laart, blombo, galeria22, nano, artsoul_artworks, sparte
from infra import gcp

# ai_data_clean.clean_materials_data()

# download all files from gcp to temporary-files folder
gcp.download_all_files('art_data_files', 'temporary-files/')