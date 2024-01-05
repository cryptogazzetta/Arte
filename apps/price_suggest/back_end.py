# External Modules
import joblib
import pandas as pd
import streamlit as st
# Project Modules
# import postgres
import github

# Import files from github
if 'lots' not in st.session_state:
    st.session_state['lots'] = pd.read_csv(github.get_file_from_github('clean-files/catalogo_artworks_info.csv'))
if 'lots_x_test' not in st.session_state:
    st.session_state['lots_x_test'] = pd.read_csv(github.get_file_from_github('analysis/models/catalogo_X_test.csv'))
if 'pricing_model' not in st.session_state:
    st.session_state['pricing_model'] = joblib.load(github.get_file_from_github('analysis/models/catalogo_xgb_model.pkl', format='pkl'))

lots = st.session_state['lots']
lots_x_test = st.session_state['lots_x_test']
pricing_model = st.session_state['pricing_model']

def clean_artists_names(lots):
    artists_list_raw = ['Di Cavalcanti (1897-1976)', 'Aldemir Martins',
        'Candido Portinari (1903-1962)', 'Milton Dacosta',
        'Antônio Bandeira (1922-1967)', 'Tarsila do Amaral',
        'Djanira da Motta e Silva',
        'Alberto Guignard - Alberto da Veiga Guignard',
        'Maria Leontina Franco Da Costa', 'Ibere Camargo - Iberê Camargo',
        'José Pancetti - Giuseppe Gianinni Pancetti - Jose Pancetti',
        'Cicero Dias - Cícero Dias', 'Cildo Meireles (1948)', 'Alfredo Volpi',
        'Annita Catarina Malfatti - Anita Malfatti - Anita Malfati',
        'Ismael Nery']

    artists_list_clean = [
                    'Di Cavalcanti',
                    'Aldemir Martins',
                    'Candido Portinari',
                    'Milton Dacosta',
                    'Antônio Bandeira',
                    'Tarsila do Amaral',
                    'Djanira',
                    'Alberto Guignard',
                    'Maria Leontina',
                    'Iberê Camargo',
                    'José Pancetti',
                    'Cícero Dias',
                    'Cildo Meireles',
                    'Alfredo Volpi',
                    'Anita Malfatti',
                    'Ismael Nery']

    mapping_dict = dict(zip(artists_list_raw, artists_list_clean))

    # Replace raw names with clean names in the 'Artist' column
    lots['Artist'] = lots['Artist'].replace(mapping_dict)

    return lots
lots = clean_artists_names(lots)

artists_list = [
    'Di Cavalcanti',
    'Aldemir Martins',
    'Candido Portinari',
    'Milton Dacosta',
    'Antônio Bandeira',
    'Tarsila do Amaral',
    'Djanira',
    'Alberto Guignard',
    'Maria Leontina',
    'Iberê Camargo',
    'José Pancetti',
    'Cícero Dias',
    'Cildo Meireles',
    'Alfredo Volpi',
    'Anita Malfatti',
    'Ismael Nery'
                ]
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

## SOLUÇÃO PROVISÓRIA: REDUZINDO O TAMANHO DA FAIXA ATÉ QUE STD < PRICE_PREDICTION
def get_price_range(price_prediction, similar_lots):
    # remove outliers: lots with price in the top 10%
    similar_lots = similar_lots[similar_lots['Price (BRL)'] <= similar_lots['Price (BRL)'].quantile(0.6)]
    similar_lots = similar_lots[similar_lots['Price (BRL)'] >= similar_lots['Price (BRL)'].quantile(0.4)]
    # Get standard deviation
    std = similar_lots['Price (BRL)'].std()

    while std > price_prediction:
        std = std / 2
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
        size_range = 0.3
        similar_lots = similar_lots[similar_lots['Height (cm)'] >= characteristics['Height (cm)']*(1-size_range)]
        similar_lots = similar_lots[similar_lots['Height (cm)'] <= characteristics['Height (cm)']*(1+size_range)]
        similar_lots = similar_lots[similar_lots['Width (cm)'] >= characteristics['Width (cm)']*(1-size_range)]
        similar_lots = similar_lots[similar_lots['Width (cm)'] <= characteristics['Width (cm)']*(1+size_range)]  

    # fill NaNs with empty string
    similar_lots.fillna('', inplace=True)

    similar_lots.set_index('Year of sale', inplace=True)
    similar_lots.sort_index(inplace=True, ascending=False)

    # drop duplicates based on url
    similar_lots.drop_duplicates(subset='url', inplace=True)

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
    # from streamlit_gsheets import GSheetsConnection
    # import ssl
    # ssl._create_default_https_context = ssl._create_unverified_context

    # # Create a connection object.
    # conn = st.connection("gsheets", type=GSheetsConnection)
    # lead_base = conn.read()

    artist = characteristics['Artist']
    medium_type = characteristics['Medium_type']
    height = characteristics['Height (cm)']
    width = characteristics['Width (cm)']
    if characteristics['Year'] != '':
        year = characteristics['Year']
    else:
        year = 'NULL'

    
    lead_info_dict = {'email': email, 'artist': artist, 'medium_type': medium_type, 'height': height, 'width': width, 'year': year}


    # add new lead info to lead_base google sheet
    # conn.query("INSERT INTO lead_base (email, artist, medium_type, height, width, year) VALUES ('{email}', '{artist}', '{medium_type}', '{height}', '{width}', '{year}')".format(**lead_info_dict))

    # postgres.create_consultation(email, artist, medium_type, height, width, year)
    
