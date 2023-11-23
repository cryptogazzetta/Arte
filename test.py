import pandas as pd
import requests
from io import StringIO

def get_file_from_github(file_path):
    url = f'https://raw.githubusercontent.com/cryptogazzetta/Arte/main/{file_path}'

    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Use StringIO to convert the response content to a file-like object
        file_content = StringIO(response.text)

        return file_content
    else:
        print(f"Failed to fetch the file. Status code: {response.status_code}")