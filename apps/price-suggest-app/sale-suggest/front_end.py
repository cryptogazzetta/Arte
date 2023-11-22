import streamlit as st
import pandas as pd
# project modules
import back_end

# user choose to input art collection manually on table or upload a csv file
# calls back_end.get_price_prediction() to get price prediction of artworks
# displays artworks with highest price difference prediction - buying price

# hide warnings
st.set_option('deprecation.showfileUploaderEncoding', False)

st.title('Art Collection Manager')

st.markdown('<h2>Manage, value and discover opportunities in your art collection.</h2>', unsafe_allow_html=True)

## DATA INPUT

st.write('You can input your art collection manually on the table below or upload a csv file.')
default_collection = [
              {'Altura': 60, 'Largura': 50, 'Artist': 'Athos Bulcão', 'Buying_Price': 10000, 'Buying_Date': '2019-01-01'},
              {'Altura': 90, 'Largura':140,'Artist': 'Adriana Varejão', 'Buying_Price': 20000, 'Buying_Date': '2001-01-01'}
              ]

user_collection = st.data_editor(default_collection, num_rows="dynamic", width=1000)

# create button to upload csv file
uploaded_file = st.file_uploader('Upload csv file', type='csv')



## DATA PROCESSING

if uploaded_file:
    user_collection = uploaded_file 



## DATA OUTPUT

# create button to get price prediction
if st.button('Get Price Prediction'):
    # add price prediction to user_collection with default data = 2*buying_price
    user_collection_df = pd.DataFrame(user_collection)

    user_collection_df['Price_Prediction'] = 2*user_collection_df['Buying_Price']
    user_collection_df['Return'] = user_collection_df['Price_Prediction'] / user_collection_df['Buying_Price'] - 1
    user_collection_df['Annualized Return'] = (1 + user_collection_df['Return'])**(1/(2021 - pd.to_datetime(user_collection_df['Buying_Date']).dt.year)) - 1
    # to %
    user_collection_df['Return'] = user_collection_df['Return'].apply(lambda x: "{:.2%}".format(x))
    user_collection_df['Annualized Return'] = user_collection_df['Annualized Return'].apply(lambda x: "{:.2%}".format(x))

    # display all artworks in table
    st.table(user_collection_df)