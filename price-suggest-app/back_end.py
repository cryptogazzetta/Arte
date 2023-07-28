import joblib
import pandas as pd

# Load the model
rf_model = joblib.load('../analysis/models/rf_model.pkl')

x = pd.read_csv('../analysis/models/x.csv')
x_columns_names = x.columns

artists_mean_price_per_inch = pd.read_csv('../analysis/models/saatchi_artists_mean_price_per_inch.csv')

def get_df_for_model(characteristics):

    if characteristics['Artist'] != None:
        artist_name = characteristics['artist']
        artist_mean_price_per_inch = artists_mean_price_per_inch['MeanPricePerInch'][artists_mean_price_per_inch['Artist'] == artist_name]

    
    test_df = pd.DataFrame(columns=x_columns_names)
    test_df.loc[0, 'Size'] = characteristics['Size']
    test_df.loc[0, 'Price / in² of other artworks by same artist'] = artist_mean_price_per_inch
    keys = list(characteristics.keys())
    
    keys.remove('Size', 'Artist')
    for criterium in keys:
        for trait in characteristics[criterium]:
            test_df.loc[0, trait] = True
    # fill all other columns with False
    test_df.fillna(False, inplace=True)
    return test_df#.values.reshape(1, -1)


def get_price_prediction(characteristics, artist_name=None):
    

    df_for_model = get_df_for_model(characteristics)

    # Make the price prediction using the trained model
    price_prediction = rf_model.predict(df_for_model.to_numpy())[0]
    return price_prediction