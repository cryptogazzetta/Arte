import joblib
import pandas as pd


# Model trained in galleries_study.ipynb
rf_model = joblib.load('../analysis/models/rf_br_marketplaces.pkl')
# Data aggregated in galleries_study.ipynb
x = pd.read_csv('../analysis/models/x_br_marketplaces.csv')

# Options for artist and gallery selectboxes
galleries = pd.read_csv('../analysis/models/galleries_br_marketplaces.csv')['0'].tolist()
artists = pd.read_csv('../analysis/models/artists_br_marketplaces.csv')['0'].tolist()


def get_input_df(characteristics):

    input_df = pd.DataFrame(columns=x.columns)

    input_df.loc[0, 'Area'] = characteristics['Area']
    if 'Artist_'+characteristics['Artist'] in x.columns:
        input_df.loc[0, characteristics['Artist']] = True
    # if 'Gallery_'+characteristics['Galeria'] in x.columns:
    #     input_df.loc[0, 'Gallery_'+characteristics['Galeria']] = True
    input_df.fillna(False, inplace=True)
    
    return input_df


def get_price_prediction(characteristics):

    input_df = get_input_df(characteristics)
    # remove columns that are not in the model
    input_df = input_df[x.columns]

    price_prediction = rf_model.predict(input_df.to_numpy())[0]

    return price_prediction