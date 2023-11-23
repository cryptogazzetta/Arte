# External modules
import streamlit as st
import locale
import pandas as pd

# Project modules
import back_end
import chart

st.set_option('deprecation.showPyplotGlobalUse', False)

# Set the locale to Brazilian Portuguese
locale.setlocale(locale.LC_NUMERIC, 'pt_BR')

st.set_page_config(
    page_title="Precificação de obras de arte",
    page_icon=":💲:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

## IMPORT STYLES FROM .CSS FILE
with open('./styles.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

## PAGE TITLE
st.markdown('<h>Marte</h>', unsafe_allow_html=True)
st.markdown(
    '<p>Criamos essa ferramenta para ajudar a precificar obras de arte com base no histórico de vendas em leilão. Fique à vontade para experimentar a ferramenta, compartilhar e propor sugestões ;) </p>',
    unsafe_allow_html=True
)

# Get lists of artists and techniques
artists_list = back_end.artists_list
techniques_list = back_end.techniques_list

#### USER INPUTS

# Artist
st.markdown('<h2>Artista</h2>', unsafe_allow_html=True)
artist = st.selectbox('Artista', artists_list, label_visibility="collapsed", index=0)

# Technique
st.markdown('<h2>Técnica</h2>', unsafe_allow_html=True)
technique = st.selectbox('Técnica', techniques_list, label_visibility="collapsed")

# Measures
col1, col2 = st.columns(2)
with col1:
    st.markdown('<h2>Altura (cm)</h2>', unsafe_allow_html=True)
    height = st.number_input('Altura', 1, 5000, 50, label_visibility="collapsed")
with col2:
    st.markdown('<h2>Largura (cm)</h2>', unsafe_allow_html=True)
    width = st.number_input('Largura', 1, 5000, 50, label_visibility="collapsed")

# E-mail
st.markdown('<h2>Seu e-mail</h2>', unsafe_allow_html=True)
email = st.text_input('E-mail', label_visibility="collapsed")

#### OUTPUTS

if st.button('Gerar relatório'):

    if not ('@' in email and '.' in email):
        st.error('Por favor, insira um e-mail válido')
        st.stop()
    else:
        pass

    characteristics = {'Artist': artist, 'Height (cm)': height, 'Width (cm)': width, 'Technique': technique.lower()}

    artist = characteristics['Artist']
    technique = characteristics['Technique']

    ## INTERACT WITH BACK-END
    back_end.save_lead(email, characteristics)
    price_prediction = back_end.get_price_prediction(characteristics)
    similar_lots = back_end.get_similar_lots(characteristics)
    similar_lots_performance = back_end.get_similar_lots_performance(similar_lots)

    if similar_lots.shape[0] == 0:
        no_similar_lots = True
    else:
        no_similar_lots = False


    st.divider()

    # SHOW PRICE SUGGESTION    
    st.markdown(f'<h1>{technique.capitalize()} por {artist}, {height}x{width}</h1>', unsafe_allow_html=True)
    if no_similar_lots:
        st.markdown(f'<p>Não encontramos obras similares no histórico de leilões.</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p>{similar_lots.shape[0]} obras similares foram encontradas no histórico.</p>', unsafe_allow_html=True)
    # Show price suggestion if all inputs are filled
    formatted_price_prediction = locale.format_string("%.0f", price_prediction, grouping=True)
    st.markdown(f'<p>Preço sugerido: R${formatted_price_prediction}</p>', unsafe_allow_html=True)


    # PLOT MARKET PERFORMANCE OF SIMILAR ARTWORKS
    st.markdown('<h2>Performance of similar artworks at auction</h2>', unsafe_allow_html=True)

    fig = chart.get_similar_lots_performance_chart(similar_lots_performance)
    st.pyplot(fig)

    # TABLE OF SIMILAR ARTWORKS AUCTIONED
    st.dataframe(similar_lots[['Technique', 'Height (cm)', 'Width (cm)', 'Price (BRL)', 'Sold']], width=1000)
