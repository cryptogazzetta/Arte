# External Modules
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
# Project Modules
import back_end
import chart

## PAGE CONFIG
st.set_page_config(
    page_title="Marte - Gestão de coleção",
    page_icon=":🎨:",
    layout="wide",
    initial_sidebar_state="collapsed"
)


## BACK END
collection = back_end.get_collection()
collection_performance = back_end.get_collection_performance(collection)
collection = back_end.get_price_prediction(collection, collection_performance)
performance_stats = back_end.get_performance_stats(collection_performance)


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

st.markdown('<h1>Performance da coleção</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([0.7, 0.3])
with col1:
    fig = chart.get_line_chart(collection_performance['Total'])
    st.pyplot(fig)
with col2:
    st.dataframe(performance_stats, width=300)

st.markdown('<h1>Obras da coleção</h1>', unsafe_allow_html=True)
st.dataframe(back_end.fix_collection_to_show(collection), width=2000)










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
