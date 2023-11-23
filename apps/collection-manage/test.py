import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

import chart

# Get data
collection = pd.read_csv('../../analysis/models/catalogo_das_artes_lots.csv')[500:512]
collection = collection[['Artist', 'Technique_fix', 'Price (BRL)', 'Height (cm)', 'Width (cm)', 'Year of sale', 'Year']]
collection.rename(columns={'Price (BRL)': 'Buying Price', 'Year of sale': 'Buying Date'}, inplace=True)


# Preprocess data
collection['Price Prediction'] = collection['Buying Price'] * np.random.uniform(0.5, 50, collection.shape[0])
collection['Return'] = collection['Price Prediction'] / collection['Buying Price'] - 1
collection['Annualized Return'] = (1 + collection['Return'])**(1/(2021 - pd.to_datetime(collection['Buying Date']).dt.year)) - 1
collection['Return'] = collection['Return'].apply(lambda x: "{:.2%}".format(x))
collection['Annualized Return'] = collection['Annualized Return'].apply(lambda x: "{:.2%}".format(x))

collection.set_index('Artist', inplace=True)


# User options
filter_by_options = ['Artista', 'Técnica']
filter_by = st.selectbox('Filtrar por', filter_by_options, index=0)

compare_by_options = ['Quantidade', 'Valor']
compare_by = st.selectbox('Comparar por', compare_by_options, index=0)

# Filter data
if compare_by == 'Quantidade':
    if filter_by == 'Artista':
        data = collection.groupby(collection.index)['Price Prediction'].count()

    elif filter_by == 'Técnica':
        data = collection.groupby('Technique_fix')['Price Prediction'].count()

elif compare_by == 'Valor':
    if filter_by == 'Artista':
        data = collection.groupby(collection.index)['Price Prediction'].sum()

    elif filter_by == 'Técnica':
        data = collection.groupby('Technique_fix')['Price Prediction'].sum()


# Display data
fig = chart.get_donut_chart(data)

# Display the plot using streamlit
st.pyplot(fig)


st.dataframe(collection)
