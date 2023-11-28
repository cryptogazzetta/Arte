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
artists_indices = pd.read_csv(get_file_from_github('analysis/models/artsy_auctions_artists_indices.csv'))
artists_indices.set_index('Year of sale', inplace=True)

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
    input_dummies = pd.get_dummies(collection.drop(columns=['Buying Date', 'Buying Price']), columns=['Artist', 'Technique'], drop_first=True)
    
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

def get_price_prediction(collection, collection_performance):
    # input_df = get_input_dummies(collection)
    # price_prediction = pricing_model.predict(input_df.to_numpy())[0]
    # # add price prediction to collection as column
    # collection['Price Prediction'] = price_prediction
    for index, artwork in collection.iterrows():
        
        collection.loc[index, 'Price Prediction'] = collection_performance.loc[2023, index]

    return collection

def get_collection_performance(collection):
    # Create DataFrame with collection artworks as columns and years in rows
    start_year = collection['Buying Date'].min()
    end_year = 2023

    # Create a list of unique artwork indices
    artwork_indices = collection.index.tolist()

    # Create a DataFrame with NaN values
    collection_performance = pd.DataFrame(index=range(start_year, end_year + 1), columns=artwork_indices)

    # Set buying price at the buying date
    for index, artwork in collection.iterrows():
        artist = artwork['Artist']
        buying_price = artwork['Buying Price']
        buying_date = artwork['Buying Date']

        collection_performance.loc[buying_date, index] = buying_price

        collection_performance.loc[buying_date+1:, index] = buying_price * artists_indices.loc[buying_date+1:, artist] / artists_indices.loc[buying_date, artist]
        
        
    # Forward fill NaN values to fill in the years
    # collection_performance.ffill(axis=0, inplace=True)

    collection_performance['Total'] = collection_performance.sum(axis=1)
    # Reset index name and convert it to a column
    collection_performance.index.name = 'Year'

    return collection_performance

def get_performance_stats(collection_performance):
    performance_stats = pd.DataFrame(index=['Return', 'Annualized Return', 'Volatility', 'Sharpe Ratio'])

    # Calculate performance metrics
    portfolio_returns = collection_performance['Total'].pct_change().dropna()
    total_return = collection_performance['Total'].iloc[-1] / collection_performance['Total'].iloc[0] - 1
    annualized_return = (1 + total_return) ** (1 / (collection_performance.index[-1] - collection_performance.index[0])) - 1
    volatility = portfolio_returns.std() * np.sqrt(252)
    sharpe_ratio = annualized_return / volatility

    # Assign values to the performance_stats DataFrame
    performance_stats.loc['Return', 'Total'] = total_return
    performance_stats.loc['Annualized Return', 'Total'] = annualized_return
    performance_stats.loc['Volatility', 'Total'] = volatility
    performance_stats.loc['Sharpe Ratio', 'Total'] = sharpe_ratio

    # first three rows as percentage
    performance_stats.iloc[:3] = performance_stats.iloc[:3].round(2)

    return performance_stats

def get_artist_performance(collection):
    artists = collection.index.unique()

def fix_collection_to_show(collection):
    collection_to_show = collection.copy()
    collection_to_show.index = collection_to_show.index.map(lambda x: f'{x:,.0f}')
    collection_to_show['Buying Price'] = collection_to_show['Buying Price'].map(lambda x: f'{x:,.0f}')
    collection_to_show['Price Prediction'] = collection_to_show['Price Prediction'].map(lambda x: f'{x:,.0f}')

    collection_to_show['Measures'] = collection_to_show['Height (cm)'].astype(str) + ' x ' + collection_to_show['Width (cm)'].astype(str)

    # change column order
    collection_to_show = collection_to_show[['Artist', 'Technique', 'Measures', 'Year', 'Buying Date', 'Buying Price', 'Price Prediction']]
    collection_to_show.rename(columns={'Price Prediction': 'Current Price Estimate'}, inplace=True)
    collection_to_show.set_index('Artist', inplace=True)

    return collection_to_show
    