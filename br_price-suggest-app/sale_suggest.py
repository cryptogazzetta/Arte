import joblib
import pandas as pd

rf_model = joblib.load('../analysis/models/rf_br_marketplaces.pkl')

x = pd.read_csv('../analysis/models/x_br_marketplaces.csv')
x_columns = x.columns

collection = [
              {'Area': 60, 'Artist': 'ATHOS BULCÃO', 'Buying_Price': 1000},
              {'Area': 90, 'Artist': 'ATHOS BULCÃO', 'Buying_Price': 2000}
              ]

def get_df_for_model(artworks_info):
    test_df = pd.DataFrame(columns=x_columns)
    for artwork in collection:
        for characteristics in artwork.keys():
            test_df.loc[0, 'Area'] = characteristics['Area']    
            test_df.loc[0, 'Artist_'+characteristics['Artist']] = True
    
    # fill all other columns with False
    test_df.fillna(False, inplace=True)
    
    return test_df


def get_price_prediction(characteristics):

    df_for_model = get_df_for_model(characteristics)
    price_prediction = rf_model.predict(df_for_model.to_numpy())[0]

    return price_prediction