import joblib
import pandas as pd

# Load the model
rf_model = joblib.load('../analysis/models/rf_model.pkl')

x = pd.read_csv('../analysis/models/x.csv')
x_columns_names = x.columns

def get_df_for_model(characteristics):
    test_df = pd.DataFrame(columns=x_columns_names)
    test_df.loc[0, 'Size'] = characteristics['Size']
    keys = list(characteristics.keys())
    keys.remove('Size')
    for criterium in keys:
        for trait in characteristics[criterium]:
            test_df.loc[0, trait] = True
    # fill all other columns with False
    test_df.fillna(False, inplace=True)
    return test_df#.values.reshape(1, -1)

def get_price_prediction(characteristics):
    df_for_model = get_df_for_model(characteristics)

    # Make the price prediction using the trained model
    price_prediction = rf_model.predict(df_for_model.to_numpy())[0]
    return price_prediction