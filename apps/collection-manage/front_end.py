import streamlit as st
import matplotlib.pyplot as plt

import back_end
import chart

## PAGE CONFIG
st.set_page_config(
    page_title="Marte - Gestão de coleção",
    layout="centered",
    initial_sidebar_state="collapsed"
)

## BACK END
collection = back_end.get_collection()

st.dataframe(collection)

collection = back_end.get_price_prediction(collection)


## Define CSS
st.set_option('deprecation.showPyplotGlobalUse', False)
css = back_end.get_file_from_github('apps/price-suggest/styles.css', format='css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

## PAGE TITLE
st.markdown('<h>Marte</h>', unsafe_allow_html=True)
st.markdown(
    '<p>Criamos essa ferramenta para ajudar a gerir coleções com base em análises quantitativas. Fique à vontade para experimentar a ferramenta, compartilhar e propor sugestões ;) </p>',
    unsafe_allow_html=True
)

st.dataframe(collection)













# # User options
# filter_by_options = ['Artista', 'Técnica']
# filter_by = st.selectbox('Filtrar por', filter_by_options, index=0)

# compare_by_options = ['Quantidade', 'Valor']
# compare_by = st.selectbox('Comparar por', compare_by_options, index=0)

# # Filter data
# if compare_by == 'Quantidade':
#     if filter_by == 'Artista':
#         data = collection.groupby(collection.index)['Year'].count()

#     elif filter_by == 'Técnica':
#         data = collection.groupby('Technique')['Year'].count()

# elif compare_by == 'Valor':
#     if filter_by == 'Artista':
#         data = collection.groupby(collection.index)['Price Prediction'].sum()

#     elif filter_by == 'Técnica':
#         data = collection.groupby('Technique')['Price Prediction'].sum()


# # Display data
# fig = chart.get_donut_chart(data)

# # Display the plot using streamlit
# st.pyplot(fig)
