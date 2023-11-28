import pandas as pd
import numpy as np
import requests
import joblib
from io import StringIO, BytesIO

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


# Import files from github
lots = pd.read_csv(get_file_from_github('clean-files/artsy_auctions_artworks_info.csv'))

lots_x_test = pd.read_csv(get_file_from_github('analysis/models/artsy_auctions_X_test.csv'))
pricing_model = joblib.load(get_file_from_github('analysis/models/artsy_auctions_gb_model.pkl', format='pkl'))


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
def get_collection():
    collection = lots[5003:5010]
    collection = collection[['Artist', 'Technique', 'Price (USD)', 'Height (cm)', 'Width (cm)', 'Year of sale', 'Year']]
    collection.rename(columns={'Price (USD)': 'Buying Price', 'Year of sale': 'Buying Date'}, inplace=True)
    return collection


def get_input_dummies(collection):
    input_dummies = pd.get_dummies(collection[['Artist', 'Technique']])
    
    # add columns height, width, year
    input_dummies['Height (cm)'] = collection['Height (cm)']
    input_dummies['Width (cm)'] = collection['Width (cm)']
    input_dummies['Year'] = collection['Year']

    print(input_dummies.columns)

    # add all columns from lots_x_test
    for column in lots_x_test.columns:
        if column not in input_dummies.columns:
            input_dummies[column] = False

    difference = set(input_dummies.columns) - set(lots_x_test.columns)
    print(difference)
    
    # By default, year of sale is 2023
    input_dummies.loc[0, 'Year of sale'] = 2023
    # Fill NaNs with False
    input_dummies.fillna(False, inplace=True)
    
    return input_dummies


def get_price_prediction(collection):
    input_df = get_input_dummies(collection)
    price_prediction = pricing_model.predict(input_df.to_numpy())[0]
    # add price prediction to collection as column
    collection['Price Prediction'] = price_prediction

    return collection

# def preprocess_data(collection):
#     collection['Price Prediction'] = 1000
#     collection['Return'] = collection['Price Prediction'] / collection['Buying Price'] - 1
#     collection['Annualized Return'] = (1 + collection['Return'])**(1/(2021 - pd.to_datetime(collection['Buying Date']).dt.year)) - 1
#     collection['Return'] = collection['Return'].apply(lambda x: "{:.2%}".format(x))
#     collection['Annualized Return'] = collection['Annualized Return'].apply(lambda x: "{:.2%}".format(x))

#     collection.set_index('Artist', inplace=True)
#     collection.sort_index(inplace=True)
#     return collection

def get_artist_performance(collection):
    artists = collection.index.unique()
    