# External Modules
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO, BytesIO
# Project Modules


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

# Import files from github
lots = pd.read_csv(get_file_from_github('clean-files/artsy_auctions_artworks_info.csv'))

lots_x_test = pd.read_csv(get_file_from_github('analysis/models/artsy_auctions_X_test.csv'))
pricing_model = joblib.load(get_file_from_github('analysis/models/artsy_auctions_gb_model.pkl', format='pkl'))

# provide lists of artists and techniques
artists_list = ['Candido Portinari', 'Marc Chagall', 'Victor Vasarely', 'Vicente do Rego Monteiro', 'Di Cavalcanti']
techniques_list = ['Print', 'Painting', 'Drawing']

# Convert to string
artists_list = [str(artist) for artist in artists_list]
techniques_list = [str(technique) for technique in techniques_list]
# Sort lists
artists_list.sort()
techniques_list.sort()

def get_input_dummies(characteristics):
    input_dummies = pd.DataFrame(columns=lots_x_test.columns)

    # Fill input_dummies with characteristics
    input_dummies.loc[0, 'Height (cm)'] = characteristics['Height (cm)']
    input_dummies.loc[0, 'Width (cm)'] = characteristics['Width (cm)']
    if 'Artist_'+characteristics['Artist'] in lots.columns:
        input_dummies.loc[0, characteristics['Artist']] = True
    if 'Technique_'+characteristics['Technique'] in lots.columns:
        input_dummies.loc[0, characteristics['Technique']] = True
    # By default, year of sale is 2023
    input_dummies.loc[0, 'Year of sale'] = 2023
    # Fill NaNs with False
    input_dummies.fillna(False, inplace=True)
    
    return input_dummies

def get_price_prediction(characteristics):
    # input_df = get_input_dummies(characteristics)
    # price_prediction = pricing_model.predict(input_df.to_numpy())[0]

    similar_lots = get_similar_lots(characteristics)
    price_prediction = similar_lots['Price (USD)'].median()

    return price_prediction

def get_similar_lots(characteristics):
    similar_lots = lots.copy()

    similar_lots.index = similar_lots.index.map(lambda x: f'{x:,.0f}')
    
    # Filter by artist
    similar_lots = similar_lots[similar_lots['Artist'] == characteristics['Artist']]
    # Filter by technique
    similar_lots = similar_lots[similar_lots['Technique'] == characteristics['Technique']]
    # Filter by size
    if characteristics['Height (cm)']:
        # Tolerance range for size
        size_range = 0.5
        similar_lots = similar_lots[similar_lots['Height (cm)'] >= characteristics['Height (cm)']*(1-size_range)]
        similar_lots = similar_lots[similar_lots['Height (cm)'] <= characteristics['Height (cm)']*(1+size_range)]
        similar_lots = similar_lots[similar_lots['Width (cm)'] >= characteristics['Width (cm)']*(1-size_range)]
        similar_lots = similar_lots[similar_lots['Width (cm)'] <= characteristics['Width (cm)']*(1+size_range)]
    

    # fill NaNs with empty string
    similar_lots.fillna('', inplace=True)

    similar_lots.set_index('Year of sale', inplace=True)
    # similar_lots.sort_index(inplace=True, ascending=False)

    return similar_lots

def get_similar_lots_performance(similar_lots):

    similar_lots_performance = similar_lots.groupby('Year of sale').agg(
        Total_Sales=('Price (USD)', 'sum'),
        Mean_Price=('Price (USD)', 'mean'),
        Sales_Count=('Price (USD)', 'count')
    ).reset_index()

    return similar_lots_performance

def save_lead(email, characteristics):
    # save to csv
    lead = pd.DataFrame(columns=['Email', 'Artist', 'Height (cm)', 'Width (cm)', 'Technique'])
    lead.loc[0, 'Email'] = email
    lead.loc[0, 'Artist'] = characteristics['Artist']
    lead.loc[0, 'Height (cm)'] = characteristics['Height (cm)']
    lead.loc[0, 'Width (cm)'] = characteristics['Width (cm)']
    lead.loc[0, 'Technique'] = characteristics['Technique']
    lead.to_csv('./lead_base.csv', mode='a', header=False, index=False)
