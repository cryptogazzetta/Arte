# External Modules
import joblib
import pandas as pd
# Project Modules
import postgres
import github


# import standard deviation
from sklearn import metrics

# Import files from github
lots = pd.read_csv(github.get_file_from_github('clean-files/catalogo_artworks_info.csv'))
lots_x_test = pd.read_csv(github.get_file_from_github('analysis/models/catalogo_X_test.csv'))
pricing_model = joblib.load(github.get_file_from_github('analysis/models/catalogo_xgb_model.pkl', format='pkl'))

# provide lists of artists and Medium_types
artists_list = lots['Artist'].unique().tolist()
medium_types_list = ['pintura']

def get_input_dummies(characteristics):
    input_dummies = pd.DataFrame(columns=lots_x_test.columns)

    # Fill input_dummies with characteristics
    input_dummies.loc[0, 'Height (cm)'] = characteristics['Height (cm)']
    input_dummies.loc[0, 'Width (cm)'] = characteristics['Width (cm)']
    if 'Artist_'+characteristics['Artist'] in lots.columns:
        input_dummies.loc[0, characteristics['Artist']] = True
    if 'Medium_type_'+characteristics['Medium_type'] in lots.columns:
        input_dummies.loc[0, characteristics['Medium_type']] = True
    
    # if characteristics['Year'] != '':
    #     input_dummies.loc[0, 'Year'] = characteristics['Year']
    # By default, year of sale is 2024
    input_dummies.loc[0, 'Year of sale'] = 2024
    # Fill NaNs with False
    input_dummies.fillna(False, inplace=True)
    
    return input_dummies

def get_price_prediction(characteristics):
    input_df = get_input_dummies(characteristics)
    price_prediction = pricing_model.predict(input_df.to_numpy())[0]
    return price_prediction

def get_price_range(price_prediction, similar_lots):
    # remove outliers: lots with price in the top 5%
    similar_lots = similar_lots[similar_lots['Price (BRL)'] <= similar_lots['Price (BRL)'].quantile(0.5)]
    # Get standard deviation
    std = similar_lots['Price (BRL)'].std()
    # Get price range
    price_range = [price_prediction-std, price_prediction+std]
    return price_range

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
        Total_Sales=('Price (BRL)', 'sum'),
        Mean_Price=('Price (BRL)', 'mean'),
        Sales_Count=('Price (BRL)', 'count'),
        # Price_m=('Price (BRL / cm)', 'mean')
    ).reset_index()

    return similar_lots_performance

def save_lead(email, characteristics):
    artist = characteristics['Artist']
    medium_type = characteristics['Medium_type']
    height = characteristics['Height (cm)']
    width = characteristics['Width (cm)']
    if characteristics['Year'] != '':
        year = characteristics['Year']
    else:
        year = 'NULL'
    postgres.create_consultation(email, artist, medium_type, height, width, year)
    
