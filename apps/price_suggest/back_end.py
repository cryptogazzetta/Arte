# External Modules
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO, BytesIO

# import postgres
import github

# Import files from github
lots = pd.read_csv(github.get_file_from_github('clean-files/artsy_auctions_artworks_info.csv'))
lots_x_test = pd.read_csv(github.get_file_from_github('analysis/models/artsy_auctions_X_test.csv'))
pricing_model = joblib.load(github.get_file_from_github('analysis/models/artsy_auctions_rf_model.pkl', format='pkl'))

# provide lists of artists and Medium_types
artists_list = ['Marc Chagall', 'Victor Vasarely']
medium_types_list = ['Painting', 'Drawing', 'Print']

def get_input_dummies(characteristics):
    input_dummies = pd.DataFrame(columns=lots_x_test.columns)

    # Fill input_dummies with characteristics
    input_dummies.loc[0, 'Height (cm)'] = characteristics['Height (cm)']
    input_dummies.loc[0, 'Width (cm)'] = characteristics['Width (cm)']
    if 'Artist_'+characteristics['Artist'] in lots.columns:
        input_dummies.loc[0, characteristics['Artist']] = True
    if 'Medium_type_'+characteristics['Medium_type'] in lots.columns:
        input_dummies.loc[0, characteristics['Medium_type']] = True
    
    if characteristics['Year'] != '':
        input_dummies.loc[0, 'Year'] = characteristics['Year']
    # By default, year of sale is 2023
    input_dummies.loc[0, 'Year of sale'] = 2023
    # Fill NaNs with False
    input_dummies.fillna(False, inplace=True)
    
    return input_dummies

def get_price_prediction(characteristics):
    input_df = get_input_dummies(characteristics)
    print(input_df.head())
    price_prediction = pricing_model.predict(input_df.to_numpy())[0]

    # similar_lots = get_similar_lots(characteristics)
    # price_prediction = similar_lots['Price (USD)'].median()

    return price_prediction

def get_similar_lots(characteristics):
    similar_lots = lots.copy()
    similar_lots.index = similar_lots.index.map(lambda x: f'{x:,.0f}')
    
    # Filter by artist
    similar_lots = similar_lots[similar_lots['Artist'] == characteristics['Artist']]
    # Filter by Medium_type
    similar_lots = similar_lots[similar_lots['Medium_type'] == characteristics['Medium_type']]
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
    similar_lots.sort_index(inplace=True, ascending=False)

    return similar_lots

def get_similar_lots_performance(similar_lots):

    similar_lots_performance = similar_lots.groupby('Year of sale').agg(
        Total_Sales=('Price (USD)', 'sum'),
        Mean_Price=('Price (USD)', 'mean'),
        Sales_Count=('Price (USD)', 'count'),
        Price_m=('Price (USD / cm)', 'mean')
    ).reset_index()

    return similar_lots_performance

def save_lead(email, characteristics):
    # save to csv
    lead = pd.DataFrame(columns=['Email', 'Artist', 'Height (cm)', 'Width (cm)', 'Medium_type', 'url'])
    lead.loc[0, 'Email'] = email
    lead.loc[0, 'Artist'] = characteristics['Artist']
    lead.loc[0, 'Height (cm)'] = characteristics['Height (cm)']
    lead.loc[0, 'Width (cm)'] = characteristics['Width (cm)']
    lead.loc[0, 'Medium_type'] = characteristics['Medium_type']
    lead.to_csv('./lead_base.csv', mode='a', header=False, index=False)
    # save to postgres
    # postgres.create_user(email, str(characteristics))
    
