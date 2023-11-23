import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import chart

collection = pd.read_csv('../../analysis/models/catalogo_das_artes_lots.csv')[500:512]

collection = collection[['Artist', 'Technique_fix', 'Price (BRL)', 'Height (cm)', 'Width (cm)', 'Year of sale', 'Year']]
# set artist as index
collection.set_index('Artist', inplace=True)


filter_by_options = ['Artista', 'Técnica']
filter_by = st.selectbox('Filtrar por', filter_by_options, index=0)

compare_by_options = ['Quantidade', 'Valor']
compare_by = st.selectbox('Comparar por', compare_by_options, index=0)

if compare_by == 'Quantidade':
    if filter_by == 'Artista':
        data = collection.groupby(collection.index)['Price (BRL)'].count()

    elif filter_by == 'Técnica':
        data = collection.groupby('Technique_fix')['Price (BRL)'].count()

elif compare_by == 'Valor':
    if filter_by == 'Artista':
        data = collection.groupby(collection.index)['Price (BRL)'].sum()

    elif filter_by == 'Técnica':
        data = collection.groupby('Technique_fix')['Price (BRL)'].sum()

fig = chart.get_donut_chart(data)

# Display the plot using streamlit
st.pyplot(fig)


st.dataframe(collection)
