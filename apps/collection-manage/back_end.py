import pandas as pd
import numpy as np

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