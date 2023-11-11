import joblib
import pandas as pd

# Load the model
rf_model = joblib.load('../analysis/models/rf_br_marketplaces.pkl')


# Load columns names of x (features) dataframe
x = pd.read_csv('../analysis/models/x_br_marketplaces.csv')
x_columns = x.columns

# Options for artist and gallery selectboxes
galleries = pd.read_csv('../analysis/models/galleries_br_marketplaces.csv')['0'].tolist()
artists = pd.read_csv('../analysis/models/artists_br_marketplaces.csv')['0'].tolist()


def get_df_for_model(characteristics):

    test_df = pd.DataFrame(columns=x_columns)
    
    test_df.loc[0, 'Area'] = characteristics['Area']    
    test_df.loc[0, 'Artist_'+characteristics['Artist']] = True
    test_df.loc[0, 'Gallery_'+characteristics['Galeria']] = True
    
    # fill all other columns with False
    test_df.fillna(False, inplace=True)
    
    return test_df


def get_price_prediction(characteristics):

    df_for_model = get_df_for_model(characteristics)
    price_prediction = rf_model.predict(df_for_model.to_numpy())[0]

    return price_prediction