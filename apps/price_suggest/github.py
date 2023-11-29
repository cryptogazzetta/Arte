# External Modules
import pandas as pd
import requests
from io import StringIO, BytesIO

def get_file_from_github(file_path, format='csv'):
    url = f'https://raw.githubusercontent.com/cryptogazzetta/Arte/main/{file_path}'

    # Make a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        if format == 'csv':
            file_content = StringIO(response.text)
        elif format == 'pkl':
            file_content = BytesIO(response.content)
        elif format in ['txt', 'css']:
            file_content = response.text

        return file_content
    else:
        print(f"Failed to fetch the file. Status code: {response.status_code}")