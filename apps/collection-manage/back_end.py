import pandas as pd
import numpy as np
import requests


## UTILS
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


## BACK END
def get_data():
    collection = pd.read_csv('../../analysis/models/catalogo_das_artes_lots.csv')[500:512]
    collection = collection[['Artist', 'Technique_fix', 'Price (BRL)', 'Height (cm)', 'Width (cm)', 'Year of sale', 'Year']]
    collection.rename(columns={'Price (BRL)': 'Buying Price', 'Year of sale': 'Buying Date'}, inplace=True)
    return collection

def preprocess_data(collection):
    collection['Price Prediction'] = collection['Buying Price'] * np.random.uniform(0.5, 50, collection.shape[0])
    collection['Return'] = collection['Price Prediction'] / collection['Buying Price'] - 1
    collection['Annualized Return'] = (1 + collection['Return'])**(1/(2021 - pd.to_datetime(collection['Buying Date']).dt.year)) - 1
    collection['Return'] = collection['Return'].apply(lambda x: "{:.2%}".format(x))
    collection['Annualized Return'] = collection['Annualized Return'].apply(lambda x: "{:.2%}".format(x))

    collection.set_index('Artist', inplace=True)
    collection.sort_index(inplace=True)
    return collection