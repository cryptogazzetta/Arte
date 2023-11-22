import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Model trained in catalogo_das_artes.ipynb
pricing_model = joblib.load('../../analysis/models/catalogo_gb_model.pkl')
# Data aggregated in catalogo_das_artes.ipynb
lots = pd.read_csv('../../analysis/models/catalogo_das_artes_lots.csv')
# x test
lots_x_test = pd.read_csv('../../analysis/models/catalogo_X_test.csv')

# provide lists of artists and techniques
artists_list = lots['Artist'].unique().tolist()
techniques_list = lots['Technique_fix'].unique().tolist()
# Convert to string
artists_list = [str(artist) for artist in artists_list]
techniques_list = [str(technique) for technique in techniques_list]
# Sort lists
artists_list.sort()
techniques_list.sort()
# Add empty option
artists_list.insert(0, ' ')
techniques_list.insert(0, ' ')

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
    input_df = get_input_dummies(characteristics)
    price_prediction = pricing_model.predict(input_df.to_numpy())[0]

    return price_prediction

def get_similar_lots(characteristics):
    similar_lots = lots
    # set id as hash of information
    similar_lots['id'] = similar_lots['Artist'] + similar_lots['Technique'] + similar_lots['Height (cm)'].astype(str) + similar_lots['Width (cm)'].astype(str)
    
    # Filter by artist
    if characteristics['Artist'] != ' ':
        similar_lots = similar_lots[similar_lots['Artist'] == characteristics['Artist']]
    # Filter by technique
    if characteristics['Technique'] != ' ':
        similar_lots = similar_lots[similar_lots['Technique_fix'] == characteristics['Technique']]
    # Filter by size
    if characteristics['Height (cm)']:
        similar_lots = similar_lots[similar_lots['Height (cm)'] >= characteristics['Height (cm)'][0]]
        similar_lots = similar_lots[similar_lots['Height (cm)'] <= characteristics['Height (cm)'][1]]
        similar_lots = similar_lots[similar_lots['Width (cm)'] >= characteristics['Width (cm)'][0]]
        similar_lots = similar_lots[similar_lots['Width (cm)'] <= characteristics['Width (cm)'][1]]
    
    # Sort by year of sale
    similar_lots = similar_lots.sort_values('Year of sale', ascending=False)
    # Reset index
    similar_lots.set_index('Year of sale', inplace=True)

    # remove duplicates (based on url)
    similar_lots.drop_duplicates(subset=['id'], inplace=True)
    similar_lots.drop(columns=['id'], inplace=True)
    # fill NaNs with empty string
    similar_lots.fillna('', inplace=True)

    # sort by index
    similar_lots.sort_index(inplace=True)

    return similar_lots

def get_similar_lots_performance(similar_lots):

    similar_lots_performance = similar_lots.groupby('Year of sale').agg(
        Total_Sales=('Price (BRL)', 'sum'),
        Mean_Price=('Price (BRL)', 'mean'),
        Sales_Count=('Price (BRL)', 'count')
    ).reset_index()

    return similar_lots_performance